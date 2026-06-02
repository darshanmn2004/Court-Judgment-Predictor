# ==========================================================
# app.py — FastAPI Backend
# Auth + Persistent History + DistilBERT + SBERT
# FINAL STABLE VERSION
# ==========================================================

import os
import uvicorn
import torch
import joblib
import numpy as np

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel

# ---------------- AUTH ----------------
from auth import router as auth_router, get_current_user

# ---------------- DB ----------------
from database import SessionLocal, engine
from models import Base, PredictionHistory

# ---------------- TRANSFORMERS ----------------
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer

# ---------------- CREATE TABLES ----------------
Base.metadata.create_all(bind=engine)

# ---------------- FASTAPI ----------------
app = FastAPI()
app.include_router(auth_router)

# ---------------- STATIC & TEMPLATES ----------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ==========================================================
# DB DEPENDENCY
# ==========================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================================
# MODEL CONFIG
# ==========================================================
MODEL_DIR = "model_artifacts"
LOCAL_BERT = "./distilbert-base-uncased"
LOCAL_SBERT = "local_sbert"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("🔥 Using device:", DEVICE)

tokenizer = AutoTokenizer.from_pretrained(LOCAL_BERT)

le_verdict = joblib.load(f"{MODEL_DIR}/le_verdict.pkl")
le_ipc = joblib.load(f"{MODEL_DIR}/le_ipc.pkl")
mlb_laws = joblib.load(f"{MODEL_DIR}/mlb_laws.pkl")
scaler_pen = joblib.load(f"{MODEL_DIR}/scaler_penalty.pkl")

# ==========================================================
# MODEL
# ==========================================================
class MultiTaskModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = AutoModel.from_pretrained(LOCAL_BERT)
        h = self.backbone.config.hidden_size
        self.drop = torch.nn.Dropout(0.2)
        self.head_v = torch.nn.Linear(h, len(le_verdict.classes_))
        self.head_i = torch.nn.Linear(h, len(le_ipc.classes_))
        self.head_l = torch.nn.Linear(h, len(mlb_laws.classes_))
        self.head_p = torch.nn.Linear(h, 1)

    def forward(self, ids, mask):
        out = self.backbone(input_ids=ids, attention_mask=mask)
        cls = self.drop(out.last_hidden_state[:, 0, :])
        return (
            self.head_v(cls),
            self.head_i(cls),
            self.head_l(cls),
            self.head_p(cls).squeeze(-1)
        )

model = MultiTaskModel().to(DEVICE)
model.load_state_dict(torch.load(f"{MODEL_DIR}/model_state.pt", map_location=DEVICE))
model.eval()
print("🔥 MODEL LOADED SUCCESSFULLY")

# ---------------- SBERT ----------------
sbert = SentenceTransformer(LOCAL_SBERT, device=DEVICE)
case_summaries = np.load(f"{MODEL_DIR}/case_summaries.npy", allow_pickle=True)
nn_model = joblib.load(f"{MODEL_DIR}/nearest_neighbors.joblib")

# ==========================================================
# HELPERS
# ==========================================================
def clean_text(t):
    return " ".join(str(t).lower().replace("\n", " ").replace("\r", " ").split())

def build_summary(facts, verdict, ipc, penalty, laws, sim):
    summary = []

    summary.append(
        f"This case is based on the following facts: {facts}."
    )

    summary.append(
        f"After examining the evidence and circumstances, the court delivered a verdict of {verdict}."
    )

    if ipc:
        summary.append(
            f"The primary IPC section applied in this case is Section {ipc}."
        )

    if laws:
        summary.append(
            f"Additional relevant legal provisions involved include Sections {', '.join(laws)}."
        )

    if penalty:
        summary.append(
            f"The punishment imposed by the court amounts to {penalty} months of imprisonment."
        )

    if sim: 
        
        summary.append(
            f"Similar past cases indicate comparable patterns such as: {sim[0]}."
        )

    return " ".join(summary)

# ==========================================================
# ROUTES
# ==========================================================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# ---------------- PREDICT ----------------
class CaseInput(BaseModel):
    case_text: str

@app.post("/predict")
def predict(
    data: CaseInput,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    text = clean_text(data.case_text)

    enc = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=256
    )

    with torch.no_grad():
        pv, pi, pl, pp = model(
            enc["input_ids"].to(DEVICE),
            enc["attention_mask"].to(DEVICE)
        )

    verdict = le_verdict.inverse_transform([pv.argmax(1).item()])[0]

    # ---------------- NOT GUILTY ----------------
    if verdict.lower() == "not guilty":
        summary = build_summary(text, "Not Guilty", None, None, None, None)
        result = {
            "verdict": "Not Guilty",
            "ipc_section": None,
            "penalty": 0,
            "relevant_laws": [],
            "similar_cases": [],
            "case_summary": summary
        }

    # ---------------- GUILTY ----------------
    else:
        ipc = le_ipc.inverse_transform([pi.argmax(1).item()])[0]

        # ---- Relevant Laws (robust) ----
        law_probs = torch.sigmoid(pl)[0].cpu().numpy()
        laws = mlb_laws.classes_[law_probs >= 0.5].tolist()

        if not laws:
            top_idx = law_probs.argsort()[-2:][::-1]
            laws = mlb_laws.classes_[top_idx].tolist()

        penalty = int(scaler_pen.inverse_transform([[pp.item()]])[0][0])

        sim_idx = nn_model.kneighbors(
            sbert.encode([text]), n_neighbors=2
        )[1][0]
        sim = [str(case_summaries[i]) for i in sim_idx]

        summary = build_summary(text, verdict, ipc, penalty, laws, sim)

        result = {
            "verdict": verdict,
            "ipc_section": ipc,
            "penalty": penalty,
            "relevant_laws": laws,
            "similar_cases": sim,
            "case_summary": summary
        }

    # ---------------- SAVE HISTORY ----------------
    history = PredictionHistory(
    user_id=user.id,
    case_text=data.case_text,
    verdict=result["verdict"],
    ipc_section=result["ipc_section"],
    penalty=result["penalty"] or 0,
    relevant_laws=",".join(result["relevant_laws"]) if result["relevant_laws"] else None,
    similar_cases="||".join(result["similar_cases"]) if result["similar_cases"] else None,
    case_summary=result["case_summary"]


    )
    db.add(history)
    db.commit()

    return result

# ---------------- HISTORY ----------------
@app.get("/history")
def history(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = (
        db.query(PredictionHistory)
        .filter(PredictionHistory.user_id == user.id)
        .order_by(PredictionHistory.created_at.desc())
        .all()
    )

    return [
        {
            "case_text": r.case_text,
            "verdict": r.verdict,
            "ipc_section": r.ipc_section,
            "penalty": r.penalty,
            "relevant_laws": r.relevant_laws.split(",") if r.relevant_laws else [],
            "similar_cases": r.similar_cases.split("||") if r.similar_cases else [],
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M"),
            "case_summary": r.case_summary
        }
        for r in records
    ]


# ---------------- RUN ----------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

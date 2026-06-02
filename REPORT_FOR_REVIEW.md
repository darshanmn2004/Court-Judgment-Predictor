## Court Judgment Predictor — Project Report

**Executive Summary:**
- **Purpose:** Predict verdict, IPC section, relevant laws (multi-label), and penalty months from a free-text `case_fact`, and retrieve similar past cases as supporting evidence.
- **Approach:** Multi-task DistilBERT backbone with four heads (verdict, IPC, laws, penalty) plus a dense retrieval pipeline based on SBERT + Nearest Neighbors. Serving via FastAPI.

**Repository Structure (key files):**
- `train.py`: Training pipeline — preprocessing, encoders, multi-task model, training loop, SBERT embedding generation, and saving artifacts to `model_artifacts/`.
- `inference.py`: Offline inference helper that mirrors `app.py` logic and prints example predictions.
- `app.py`: FastAPI server exposing `POST /predict` and UI endpoints; loads artifacts from `model_artifacts/`.
- `preprocess.py`: Text cleaning helper.
- `dataset_generator.py`: Synthetic dataset generator creating `balanced_final_dataset_v6.csv`.
- `model_artifacts/`: Saved model state, encoders, tokenizer, SBERT artifacts, embeddings, and nearest-neighbor index.

**Data & Preprocessing:**
- **Data:** `balanced_final_dataset_v6.csv` — synthetic balanced dataset of Guilty/Not Guilty cases spanning ~25+ IPCs. Columns include `case_id`, `case_fact`, `verdict`, `ipc_section`, `relevant_laws`, `penalty_months`, and `similar_case_summaries`.
- **Preprocess:** Current cleaning normalizes casing and whitespace and removes line breaks. Tokenization uses `AutoTokenizer` with `max_length=256`, `padding='max_length'` and `truncation=True`.
- **Labels:** `LabelEncoder` for `verdict` & `ipc`, `MultiLabelBinarizer` for laws, `MinMaxScaler` for penalty months.

**Modeling & Training:**
- **Architecture:** Shared DistilBERT backbone → dropout → four linear heads.
- **Loss:** CrossEntropy (verdict, IPC) + BCEWithLogits (laws, per-label `pos_weight`) + MSE (penalty). Overall: loss_v + loss_i + LAW_LOSS_WEIGHT * loss_l + loss_p. `LAW_LOSS_WEIGHT` default = 2.0.
- **Training settings:** Batch size 8, epochs 4, LR 3e-5, warmup 6% steps, AMP enabled on GPU, seed=42. Train/val split 85/15 stratified by verdict.

**Retrieval:**
- SBERT (`all-MiniLM-L6-v2`) encodes `case_fact` into `case_embeddings.npy`. `NearestNeighbors(metric='cosine')` saved as `nearest_neighbors.joblib` serves top-k similar cases; `case_summaries.npy` stores display summaries.

**Inference Behavior:**
- Input cleaned & tokenized → model predicts logits for all heads.
- Verdict: argmax → decode. If `Not Guilty`, `app.py` short-circuits (no IPC/laws/penalty).
- IPC: argmax of IPC head.
- Laws: sigmoid on logits; serving threshold 0.5 (validation reported at 0.25). If none pass, `app.py` returns top-3 by probability.
- Penalty: inverse-transform scaled prediction via `scaler_penalty` and round.

**Artifacts & Reproducibility:**
- Saved artifacts in `model_artifacts/`: `model_state.pt`, `le_verdict.pkl`, `le_ipc.pkl`, `mlb_laws.pkl`, `scaler_penalty.pkl`, `case_embeddings.npy`, `case_ids.npy`, `case_summaries.npy`, `nearest_neighbors.joblib`, and tokenizer files.
- `tokenizer.save_pretrained(OUT_DIR)` is called during training to ensure tokenizer reproducibility.

**Known Issues & Recommendations (short):**
- Move hardcoded secrets (JWT `SECRET_KEY`) to environment variables; use `pydantic` settings.
- Unify short-circuit semantics between `app.py` and `inference.py` (use `None` vs `0`).
- Replace sklearn `NearestNeighbors` with FAISS/HNSW for production-scale retrieval.
- Tune per-label thresholds for `relevant_laws` on validation set rather than using a global 0.5.
- Add unit tests for `preprocess` and `parse_laws` and add a CI workflow to run them.

**Evaluation Strategy:**
- Verdict & IPC: report accuracy, macro/micro F1, and confusion matrices.
- Laws (multi-label): per-label precision, recall, F1, PR-AUC; tune per-label thresholds on validation.
- Penalty: RMSE, MAE, group error by severity buckets (High/Medium/Low).

**Productionization Roadmap (concise):**
- **P0 (1–3 days):** Move secrets to env vars; add `/health` check; add unit tests and CI skeleton.
- **P1 (1–2 weeks):** Per-label threshold tuning; convert retrieval to FAISS; integrate experiment tracking (wandb/MLflow).
- **P2 (3–6 weeks):** Backbone experiments (LegalBERT / LoRA); implement explainability (Integrated Gradients) and human-in-the-loop labeling UI.
- **P3 (6–12 weeks):** Containerize with GPU support, autoscale via Kubernetes, export model to ONNX/Triton for low-latency inference, and deploy vector DB (Milvus/Pinecone) if needed.

**Quick Commands**
- Create & activate venv (PowerShell):
```
python -m venv venv
& .\\venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```
- Run API locally:
```
setx SECRET_KEY "your-secret"
uvicorn app:app --reload
```
- Train (dev):
```
python train.py
```

**Next Steps (I can implement):**
- Implement P0 (move `SECRET_KEY` to env, add `/health` endpoint, add unit tests and CI skeleton) — recommended immediate task.
- Implement per-label threshold tuning script and produce a CSV of suggested thresholds.
- Replace sklearn retrieval with FAISS and benchmark retrieval latency.

---

If you'd like, I can now implement P0 (safety + tests + CI skeleton). Tell me to proceed and I'll make the code changes and add tests.

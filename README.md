# ⚖️ Court Judgment Prediction System

An AI-powered legal analytics platform that predicts court judgment outcomes, IPC sections, relevant laws, penalties, and retrieves similar historical cases using DistilBERT and SBERT.

---

## 📌 Project Overview

The Court Judgment Prediction System assists legal professionals, students, and researchers by analyzing case descriptions and predicting:

- Verdict (Guilty / Not Guilty)
- IPC Section
- Relevant Laws
- Penalty Duration
- Detailed Case Summary
- Similar Historical Cases

The system uses Natural Language Processing (NLP), Transformer Models, and Semantic Similarity Search to provide intelligent legal predictions.

---

## 🚀 Features

### 🔐 User Authentication
- User Registration
- Secure Login
- JWT Authentication
- Session Management

### ⚖️ Legal Prediction Engine
- Verdict Prediction
- IPC Section Prediction
- Relevant Law Prediction
- Penalty Prediction

### 📝 Case Summary Generation
Automatically generates a detailed legal summary including:
- Facts of the case
- Predicted verdict
- IPC sections involved
- Relevant laws
- Predicted punishment

### 🔍 Similar Case Retrieval
Uses SBERT embeddings and Nearest Neighbors search to find legally similar historical cases.

### 📜 Prediction History
- Stores user predictions permanently
- View previous predictions after re-login
- History linked to each user account

---

## 🧠 Machine Learning Architecture

### DistilBERT Multi-Task Learning

The model simultaneously predicts:

| Task | Output |
|--------|----------|
| Verdict | Guilty / Not Guilty |
| IPC Section | IPC Classification |
| Relevant Laws | Multi-label Classification |
| Penalty | Regression |

### SBERT Similarity Search

Used for:

- Semantic case representation
- Similar case retrieval
- Legal precedent analysis

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- FastAPI
- Python

### Database
- SQLite
- SQLAlchemy ORM

### AI / ML
- PyTorch
- Transformers
- DistilBERT
- Sentence-BERT (SBERT)
- Scikit-Learn

---

## 📂 Project Structure

```text
Court-Judgment-Predictor/
│
├── app.py
├── auth.py
├── database.py
├── models.py
├── create_tables.py
│
├── templates/
│   ├── index.html
│   ├── auth.html
│   └── dashboard.html
│
├── static/
│
├── model_artifacts/
│
├── distilbert-base-uncased/
│
├── local_sbert/
│
├── requirements.txt
├── README.md
└── court_judgment.db
```

---

## 📊 Prediction Output Example

```json
{
  "verdict": "Guilty",
  "ipc_section": "326",
  "penalty": 47,
  "relevant_laws": [
    "278",
    "289",
    "304B",
    "324"
  ],
  "similar_cases": [
    "Case involving digital records.",
    "Case involving witness testimony.",
    "Case involving forensic evidence."
  ],
  "case_summary": "The court delivered a verdict of Guilty..."
}
```

---

# 📸 Screenshots

## 🏠 Home Page


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8083dd61-a3e8-4082-8f25-e9bac0380534" />

---

## 🔑 Login & Registration

![Login](screenshots/login.png)

---

## 📋 Dashboard

![Dashboard](screenshots/dashboard.png)

---

## ⚖️ Prediction Result

![Prediction](screenshots/prediction.png)

---

## 🔍 Similar Cases

![Similar Cases](screenshots/similar_cases.png)

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/darshanmn2004/Court-Judgment-Predictor.git

cd Court-Judgment-Predictor
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

or

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## 📈 Future Enhancements

- Indian Case Law Dataset Integration
- Legal Citation Extraction
- Explainable AI Predictions
- Court Precedent Recommendation
- PDF Judgment Upload
- Multilingual Support
- Advanced Legal Analytics Dashboard

---

## 🎯 Learning Outcomes

This project demonstrates:

- Natural Language Processing (NLP)
- Transformer Models
- DistilBERT Fine-Tuning
- Sentence-BERT Embeddings
- Multi-Task Learning
- FastAPI Development
- Authentication Systems
- Database Integration
- Similarity Search
- Full Stack AI Application Development

---

## 👨‍💻 Author

### Darshan MN

Bachelor of Computer Applications (BCA)

Skills:
- Python
- Machine Learning
- FastAPI
- Java
- Spring Boot
- PostgreSQL
- Manual Testing
- Hibernate
- JDBC

GitHub:
https://github.com/darshanmn2004

LinkedIn:
www.linkedin.com/in/darshan-mn-07797a285

---

## 📜 License

This project is developed for educational and research purposes.

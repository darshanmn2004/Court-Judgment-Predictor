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

## 🤗 Hugging Face Model Repository

To keep this GitHub repository lightweight and maintainable, the trained machine learning models and artifacts are hosted separately on Hugging Face.

### Hosted Components

| Component               | Description                                                          |
| ----------------------- | -------------------------------------------------------------------- |
| DistilBERT Model        | Fine-tuned transformer model for legal prediction                    |
| SBERT Model             | Semantic similarity search model                                     |
| Model Artifacts         | Trained weights, label encoders, scalers, and nearest-neighbor model |
| Preprocessing Artifacts | Text preprocessing resources and metadata                            |

### Hugging Face Repository

**Model Repository:**
https://huggingface.co/Darshanmn17/court-judgment-predictor-models

### Prediction Capabilities

The hosted models are used to perform:

* Verdict Prediction
* IPC Section Prediction
* Relevant Law Prediction
* Penalty Prediction
* Similar Case Retrieval
* Detailed Case Summary Generation

### Storage Architecture

| Resource         | Platform     |
| ---------------- | ------------ |
| Source Code      | GitHub       |
| Frontend         | GitHub       |
| Backend API      | GitHub       |
| Database Schema  | GitHub       |
| DistilBERT Model | Hugging Face |
| SBERT Model      | Hugging Face |
| Model Artifacts  | Hugging Face |

This architecture follows industry best practices by separating source code from large machine learning models.


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
 ## 🔄 System Workflow

1. User Registration/Login
2. User enters case facts
3. DistilBERT processes the legal text
4. Verdict Prediction is generated
5. IPC Section is predicted
6. Relevant Laws are identified
7. Penalty is estimated
8. SBERT retrieves similar historical cases
9. Detailed case summary is generated
10. Prediction is stored in SQLite database
11. User can access predictions from the History panel

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
## 🗄️ Database Design

The project uses SQLite with SQLAlchemy ORM.

### Tables

#### users

Stores user authentication information.

Fields:

* id
* full_name
* email
* password_hash

#### prediction_history

Stores prediction history for each user.

Fields:

* id
* user_id
* case_text
* verdict
* ipc_section
* penalty
* relevant_laws
* case_summary
* similar_cases
* created_at

### Benefits

* Persistent history after re-login
* User-specific prediction records
* Lightweight local database
* Easy deployment


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

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/76fad30b-6105-4974-8f45-5351de922b87" />


---

## 📋 Dashboard

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1fa3f035-f3de-48ea-9f07-7d884f3d0b9c" />


---

## ⚖️ Prediction Result

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6b57fec1-248c-49da-8f5f-69f5c8c6886f" />


---

## 🔍 Similar Cases

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/51ff5f32-e5be-4dae-8d55-c565b906c73b" />


---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/darshanmn2004/Court-Judgment-Predictor.git

cd Court-Judgment-Predictor
```

### Download Model Files

The trained AI models are hosted separately on Hugging Face due to their large size.

Download the following files:

- distilbert-base-uncased.zip
- local_sbert.zip
- model_artifacts.zip
- preprocessing_artifacts.zip

### Hugging Face Repository

https://huggingface.co/Darshanmn17/court-judgment-predictor-models

### Extract Model Files

Extract all downloaded ZIP files into the project root directory.

After extraction, your project structure should look like:

```text
Court-Judgment-Predictor/
│
├── app.py
├── auth.py
├── database.py
├── models.py
├── create_tables.py
│
├── distilbert-base-uncased/
├── local_sbert/
├── model_artifacts/
├── preprocessing_artifacts/
│
├── templates/
├── static/
├── requirements.txt
└── README.md
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

### Open in Browser

```text
http://127.0.0.1:8000
```

### Usage

1. Register a new account.
2. Login to the system.
3. Enter case facts in the dashboard.
4. Click **Predict Judgment**.
5. View:
   - Verdict Prediction
   - IPC Section
   - Relevant Laws
   - Penalty
   - Detailed Case Summary
   - Similar Cases
6. Access previous predictions from the History sidebar.

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

## 🔗 Project Links

### GitHub Repository

https://github.com/darshanmn2004/Court-Judgment-Predictor

### Hugging Face Repository

https://huggingface.co/Darshanmn17/court-judgment-predictor-models


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

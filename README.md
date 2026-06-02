# Court Judgment Predictor

An AI-powered Court Judgment Prediction System built using FastAPI, DistilBERT, SBERT, and Machine Learning.

## Features

* User Authentication
* Court Judgment Prediction
* IPC Section Prediction
* Relevant Law Prediction
* Penalty Prediction
* Similar Case Retrieval
* Case Summary Generation
* Persistent Prediction History

## Tech Stack

* Python
* FastAPI
* DistilBERT
* Sentence-BERT (SBERT)
* SQLite
* HTML/CSS/JavaScript

## Model Files

The trained model files are hosted on Hugging Face:

https://huggingface.co/Darshanmn17/court-judgment-predictor-models

Download and extract:

* distilbert-base-uncased
* local_sbert
* model_artifacts
* preprocessing_artifacts

Place them in the project root directory.

## Run Project

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Open:

http://127.0.0.1:8000

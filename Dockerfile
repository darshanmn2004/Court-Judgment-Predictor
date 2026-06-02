FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and install CPU-only PyTorch from official index, then other Python deps
RUN pip install --upgrade pip setuptools wheel
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch
RUN pip install fastapi uvicorn[standard] transformers "sentence-transformers>=2.2.2" numpy scikit-learn joblib jinja2 pydantic

# Copy project files (models and assets may be large — consider mounting instead)
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

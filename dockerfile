# Python ka base image
FROM python:3.11-slim

# System dependencies (OCR ke liye zaroori)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pura code copy karo
COPY . .

# FastAPI start karo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
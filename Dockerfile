FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (Tesseract, PDF tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Environment variables for optimization
ENV TRANSFORMERS_NO_ADVISORY_WARNINGS=1
ENV TOKENIZERS_PARALLELISM=false
ENV PYTHONUNBUFFERED=1

# Copy requirements
COPY requirements.txt ./

# Install dependencies (no PyTorch for lightweight deployment)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./backend ./backend
COPY ./frontend ./frontend
COPY ./data ./data

# Expose port (Render will override with $PORT)
EXPOSE 8000

# Start server with dynamic port binding
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]


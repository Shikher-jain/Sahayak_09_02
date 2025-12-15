FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better Docker cache usage
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ./backend ./backend
COPY ./frontend ./frontend
COPY ./data ./data

EXPOSE 7860

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]

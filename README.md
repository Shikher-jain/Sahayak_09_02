# Multilingual AI Teaching Assistant

## Project Structure

```
ai-teacher/
│
├── backend/
│   ├── main.py
│   ├── rag_engine.py
│   ├── extractor.py
│   ├── embedder.py
│   ├── db.py
│   ├── finetune_prompt.py
│   ├── requirements.txt
│
├── data/
│   ├── fine_tune_dataset.jsonl
│
├── frontend/
│   ├── app.py  (Streamlit)
│
└── README.md
```

## Roadmap

1. Extract text from PDF, image, audio, URL, YouTube
2. Chunk and embed text (OpenAI embeddings, store in Qdrant)
3. RAG retrieval (query → embedding → top-k docs)
4. Fine-tune model (OpenAI JSONL format)
5. FastAPI backend endpoints: /upload, /ask, /summarize, /ocr, /finetune/status
6. Streamlit UI

## Deployment

- Backend: Deploy with uvicorn on Render, Railway, AWS EC2
- Frontend: Deploy Streamlit on Streamlit Cloud or Render
- Configure CORS for frontend-backend communication

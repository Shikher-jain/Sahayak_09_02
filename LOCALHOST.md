# 🏠 LOCAL DEVELOPMENT GUIDE

## ✅ Complete Setup for Localhost

### Prerequisites:
1. **Python 3.8+** installed
2. **Tesseract OCR** installed (for image OCR)
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Add to PATH: `C:\Program Files\Tesseract-OCR`
3. **Git Bash** or **MinGW64** (for Cosdata on Windows)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start Cosdata Vector Database

**Windows (Git Bash/MINGW64):**
```bash
start-cosdata
# Enter admin key: admin
```

**Docker Alternative:**
```bash
docker run -d --name cosdata-server -p 8443:8443 -p 50051:50051 cosdataio/cosdata:latest
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- ✅ FastAPI + Uvicorn (backend)
- ✅ Streamlit (frontend)
- ✅ Sentence-Transformers (ML embeddings)
- ✅ PyMuPDF (PDF extraction)
- ✅ Pytesseract (OCR)
- ✅ All other dependencies

### Step 3: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend  
streamlit run app.py
```

**Open:** http://localhost:8501

---

## 📊 Project Structure

```
sahayak_09_02/
├── backend/
│   ├── main.py           # FastAPI app (localhost optimized)
│   ├── db.py             # Cosdata client with fallback
│   ├── embedder.py       # Sentence-transformers embeddings
│   ├── extractor.py      # PDF/OCR extraction
│   └── rag_engine.py     # RAG logic
├── frontend/
│   └── app.py            # Streamlit UI
├── data/
│   └── pdf_storage/      # Uploaded files
├── deployment/           # 🚀 Deployment files (separate)
│   ├── Dockerfile
│   ├── render.yaml
│   ├── main.py          # Deployment-optimized backend
│   ├── embedder.py      # Switchable embeddings
│   └── README.md        # Deployment guide
├── requirements.txt      # Localhost dependencies (with ML)
├── README.md            # Main documentation
└── LOCALHOST.md         # This file

```

---

## 🔧 Configuration

### Backend Configuration:
- **Port:** 8000
- **Host:** 0.0.0.0 (accessible from network)
- **Auto-reload:** Enabled (for development)

### Cosdata Configuration:
- **URL:** http://127.0.0.1:8443
- **Admin Key:** admin (default)
- **Collection:** pdf_documents

### Environment Variables (Optional):
Create `.env` file:
```env
COSDATA_URL=http://127.0.0.1:8443
COSDATA_API_KEY=admin
```

---

## 🧪 Testing

### Test Backend:
```bash
# Health check
curl http://localhost:8000/health

# Upload PDF
curl -X POST http://localhost:8000/upload -F "file=@test.pdf"

# Ask question
curl "http://localhost:8000/ask?question=What is this about?"
```

### Test Frontend:
1. Open http://localhost:8501
2. Upload a PDF or image
3. Ask questions
4. View answers

### Run System Test:
```bash
python test_system.py sample.pdf
```

---

## 🎯 Features (Localhost)

### ✅ Full ML Capabilities:
- Sentence-Transformers (all-MiniLM-L6-v2)
- 384-dimensional embeddings
- Cosine similarity search

### ✅ Document Processing:
- PDF text extraction (PyMuPDF)
- Image OCR (Tesseract)
- Smart chunking (800 chars, 100 overlap)

### ✅ Vector Search:
- Cosdata OSS Vector DB
- Automatic fallback to in-memory storage
- Top-K semantic search

### ✅ API Endpoints:
- `POST /upload` - Upload documents
- `GET /ask` - Query documents
- `GET /health` - Health check
- `GET /` - API info

---

## 🐛 Troubleshooting

### Cosdata Not Connecting?
```bash
# Check if running
curl http://127.0.0.1:8443

# Restart
start-cosdata
```

### Port Already in Use?
```bash
# Backend on different port
uvicorn backend.main:app --port 8001

# Frontend on different port
streamlit run frontend/app.py --server.port 8502
```

### Import Errors?
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### OCR Not Working?
1. Install Tesseract
2. Add to PATH
3. Restart terminal

---

## 🔄 Development Workflow

### 1. Make Changes:
- Edit backend code in `backend/`
- Edit frontend code in `frontend/`
- Backend auto-reloads (--reload flag)
- Frontend auto-reloads (Streamlit feature)

### 2. Test Changes:
- Upload test documents
- Query and verify results
- Check terminal logs

### 3. Commit:
```bash
git add .
git commit -m "Your changes"
git push
```

---

## 📈 Performance Tips

### Speed Up Model Loading:
```python
# In embedder.py - model is lazy-loaded automatically
# First request loads model, subsequent requests use cached model
```

### Optimize Chunking:
```python
# In main.py - adjust chunk size/overlap
chunk_size = 800  # Larger = more context
overlap = 100     # Larger = better continuity
```

### Improve Search:
```python
# In rag_engine.py - adjust top_k
top_k = 5  # Higher = more context, slower
```

---

## 🚀 Ready for Deployment?

When you're ready to deploy:

1. **Check deployment folder:** `cd deployment/`
2. **Read deployment guide:** `deployment/README.md`
3. **Follow deployment instructions**

---

## 💡 Tips

- Keep Cosdata running in background
- Use `--reload` for backend development
- Streamlit auto-reloads on file changes
- Check logs for debugging
- Test with sample PDFs first

---

## 🎉 You're Ready!

Everything is configured for localhost development:
- ✅ Full ML model
- ✅ Immediate initialization
- ✅ Auto-reload enabled
- ✅ Clean separation from deployment code

**Start coding and enjoy! 🚀**

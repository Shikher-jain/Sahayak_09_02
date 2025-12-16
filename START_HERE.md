# 🚀 QUICK START - Localhost

## 3 Commands to Run:

```bash
# Terminal 1: Start Cosdata (Git Bash)
start-cosdata
# Enter: admin

# Terminal 2: Start Backend (from project root)
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3: Start Frontend
cd frontend && streamlit run app.py
```

**Open:** http://localhost:8501

---

## 📁 Project Organization:

```
📂 Root - Localhost Development (this is what you use!)
├── backend/          → Backend API (optimized for local)
├── frontend/         → Streamlit UI (enhanced)
├── data/            → Uploaded files storage
├── requirements.txt  → Full dependencies (with ML)
└── LOCALHOST.md     → Full localhost guide

📂 deployment/       → Deployment Only (ignore for local dev)
├── main.py          → Deployment-optimized backend
├── embedder.py      → Switchable embeddings
├── Dockerfile       → Docker container
├── render.yaml      → Render.com config
└── README.md        → Deployment instructions
```

---

## ✅ What's Optimized for Localhost:

### Backend (`backend/`):
- ✅ Full ML model (sentence-transformers)
- ✅ Immediate initialization
- ✅ Auto-reload enabled
- ✅ Clean code (no deployment hacks)

### Frontend (`frontend/`):
- ✅ Enhanced UI with metrics
- ✅ Backend status indicator
- ✅ Better error messages
- ✅ Progress spinners

### Dependencies (`requirements.txt`):
- ✅ All ML libraries included
- ✅ PyTorch for embeddings
- ✅ Full feature set

---

## 🔧 Configuration:

**No .env file needed!** Everything uses defaults:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:8501`
- Cosdata: `http://127.0.0.1:8443`

---

## 🎯 Features:

- 📄 PDF text extraction
- 🖼️ Image OCR
- 🧠 ML embeddings (384-dim)
- 💾 Cosdata vector DB
- 🔍 Semantic search
- ⚡ Auto-reload (dev mode)

---

## 📚 Documentation:

- **LOCALHOST.md** - Complete localhost guide (read this!)
- **README.md** - Project overview
- **deployment/README.md** - Deployment guide (when ready)
- **COSDATA_SETUP.md** - Cosdata installation

---

## 🆘 Quick Fixes:

**Backend not starting?**
```bash
pip install -r requirements.txt
```

**Cosdata not connecting?**
```bash
# Check if running
curl http://127.0.0.1:8443

# Restart
start-cosdata
```

**Port conflict?**
```bash
# Use different port
uvicorn backend.main:app --port 8001
```

---

**Everything is ready for localhost development! 🎉**

# Sahayak AI - Quick Start Guide

## 🚀 Running the Complete Project

### **Option 1: One-Click Startup (Recommended)**

Double-click: **`run_all.bat`**

This will:
- ✅ Start Cosdata Vector DB (Docker)
- ✅ Start FastAPI Backend (port 8000)
- ✅ Start Streamlit Frontend (port 8501)
- ✅ Open the app in your browser

---

### **Option 2: Manual Startup**

#### **Step 1: Start Cosdata**
```bash
docker-compose up -d cosdata
```

#### **Step 2: Start Backend**
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

#### **Step 3: Start Frontend**
```bash
streamlit run frontend/app.py
```

---

## 🛑 Stopping All Services

Double-click: **`stop_all.bat`**

Or manually:
```bash
docker-compose down
# Then close the terminal windows
```

---

## 🔍 Checking Service Status

Double-click: **`check_status.bat`**

This shows:
- Docker status
- Cosdata container status
- Backend status (port 8000)
- Frontend status (port 8501)

---

## 📡 Service URLs

| Service | URL |
|---------|-----|
| **Frontend (Streamlit)** | http://localhost:8501 |
| **Backend API** | http://localhost:8000 |
| **API Documentation** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health |
| **Cosdata Vector DB** | http://localhost:8443 |

---

## 🐛 Troubleshooting

### Backend shows "Cosdata not reachable"
1. Check if Cosdata container is running: `docker ps`
2. Restart Cosdata: `docker-compose restart cosdata`
3. Wait 10 seconds for Cosdata to initialize

### Port already in use
- Stop all services: `stop_all.bat`
- Check for zombie processes: `check_status.bat`
- Kill specific port (example for 8000):
  ```bash
  netstat -ano | findstr :8000
  taskkill /F /PID <PID>
  ```

### Docker not running
- Start Docker Desktop
- Wait for Docker to fully initialize
- Run `run_all.bat` again

---

## 📁 Project Structure

```
sahayak_09_02/
├── run_all.bat          # 🚀 Start everything
├── stop_all.bat         # 🛑 Stop everything
├── check_status.bat     # 🔍 Check service status
├── backend/
│   ├── main.py          # FastAPI app
│   ├── db.py            # Cosdata client
│   ├── embedder.py      # Embedding model
│   ├── extractor.py     # PDF/Image extraction
│   └── rag_engine.py    # RAG pipeline
├── frontend/
│   └── app.py           # Streamlit UI
├── docker-compose.yml   # Docker orchestration
└── requirements.txt     # Python dependencies
```

---

## ⚡ Quick Commands

| Task | Command |
|------|---------|
| Start all | `run_all.bat` |
| Stop all | `stop_all.bat` |
| Check status | `check_status.bat` |
| View logs | `docker-compose logs -f cosdata` |
| Restart Cosdata | `docker-compose restart cosdata` |

---

## 🎯 Development vs Production

### Development (with auto-reload)
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Production (no reload - more stable)
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Note:** `run_all.bat` uses production mode for stability.

---

## 🔥 First Time Setup

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Tesseract OCR** (for image extraction)
   - Download: https://github.com/UB-Mannheim/tesseract/wiki
   - Add to PATH

3. **Start Docker Desktop**

4. **Run the project**
   ```bash
   run_all.bat
   ```

---

## ✅ System Requirements

- ✅ Python 3.11+
- ✅ Docker Desktop
- ✅ 4GB RAM minimum
- ✅ Tesseract OCR (for image processing)

---

**For detailed documentation, see:**
- `START_HERE.md` - Full project overview
- `DOCKER_GUIDE.md` - Docker setup details
- `LOCALHOST.md` - Local development guide

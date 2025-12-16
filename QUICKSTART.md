# 🚀 QUICK START GUIDE

## Start in 3 Steps:

### Step 1: Start Cosdata Vector DB

**Git Bash/MINGW64:**
```bash
start-cosdata
```
Enter admin key: `admin`

**Or Docker:**
```powershell
docker run -d --name cosdata-server -p 8443:8443 -p 50051:50051 cosdataio/cosdata:latest
```

### Step 2: Install & Start Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Start backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Start Frontend

**New terminal:**
```bash
cd frontend
streamlit run app.py
```

**Open:** http://localhost:8501

---

## 📊 Complete Workflow Test

1. **Upload a PDF** through the web UI
2. **Ask questions** about the content
3. **Get accurate answers** from semantic search

---

## ✅ Verify Installation

```bash
# Test the system
python test_system.py sample.pdf
```

---

## 🔧 Troubleshooting

### Cosdata not connecting?
```bash
# Check if running
curl http://127.0.0.1:8443

# Restart
start-cosdata
```

### Backend not starting?
```bash
# Check port
netstat -ano | findstr :8000

# Use different port
uvicorn backend.main:app --port 8001
```

---

## 📚 Architecture

```
USER → Streamlit UI → FastAPI → Cosdata Vector DB
          ↓              ↓              ↓
      Upload PDF    Extract Text    Store Embeddings
      Ask Question  Search Similar  Retrieve Chunks
```

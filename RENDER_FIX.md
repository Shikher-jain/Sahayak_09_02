# ⚠️ CRITICAL RENDER DEPLOYMENT FIXES

## Issues Fixed:

### 1. ✅ Lazy Model Loading
- `embedder.py` now loads model ONLY on first request
- Prevents OOM during startup

### 2. ✅ CPU-Only Torch
- Dockerfile installs CPU-only PyTorch
- Prevents CUDA bloat (saves ~2GB RAM)

### 3. ✅ Startup Event
- `init_db()` moved to FastAPI `@app.on_event("startup")`
- Server binds to port FIRST, then initializes services

### 4. ✅ Memory Optimization
- Added env vars: `TRANSFORMERS_NO_ADVISORY_WARNINGS`, `TOKENIZERS_PARALLELISM`
- Removed duplicate `httpx` from requirements

### 5. ✅ System Dependencies
- Dockerfile includes Tesseract OCR
- Properly configured for Render

---

## 🚨 IMPORTANT: Render Free Tier Won't Work

**Your app requires:**
- ~1.5-2GB RAM for sentence-transformers
- Render Free: 512MB RAM ❌

**Solutions:**

### Option A: Upgrade Render (Recommended)
- **Starter Plan: $7/month** (512MB → 1GB)
- Should work with optimizations

### Option B: Use Alternative (FREE)
- **Hugging Face Spaces** ← BEST for ML apps
- **Railway** ($5 credit/month)
- **Fly.io** (generous free tier)

---

## 📦 Deploy to Hugging Face Spaces (FREE & ML-Optimized)

1. Go to https://huggingface.co/spaces
2. Create new Space → Select "Gradio" or "Streamlit"
3. Upload:
   - `requirements.txt`
   - `packages.txt`
   - Your code
4. Done! HF handles ML dependencies automatically

---

## 🔧 If Using Render Paid Plan:

```bash
git add .
git commit -m "Fix Render OOM: lazy loading, CPU torch, startup optimization"
git push
```

Then in Render dashboard:
- Clear build cache
- Redeploy
- Wait 5-10 minutes (model downloads on first request)

---

## ✅ Test Locally First:

```bash
# Build Docker image
docker build -t sahayak-test .

# Run with limited memory (simulate Render)
docker run -p 8000:8000 -e PORT=8000 --memory="1g" sahayak-test
```

If it runs locally with 1GB RAM, it'll work on Render Starter.

---

## 💡 Pro Recommendation:

**Split architecture (ALL FREE):**
- Frontend: Streamlit Cloud (FREE)
- API: Render/Railway (handles uploads)
- ML Inference: HF Inference API (FREE)

This way you avoid hosting heavy ML models yourself.

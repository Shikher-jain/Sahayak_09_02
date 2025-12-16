# 🚀 Deployment Instructions

## Files in this folder:

- `Dockerfile` - Docker container configuration
- `render.yaml` - Render.com deployment config
- `requirements.txt` - Lightweight dependencies (no ML)
- `main.py` - FastAPI with startup events (deployment-optimized)
- `embedder.py` - Switchable embeddings (ML or lightweight)
- `apt-packages.txt` - System packages for Render
- `packages.txt` - Tesseract for Streamlit Cloud

## Quick Deploy Options:

### Option 1: Render.com (Recommended)

1. Push code to GitHub
2. Go to https://dashboard.render.com
3. New Web Service → Connect repo
4. Use these settings:
   - Build: `pip install -r deployment/requirements.txt`
   - Start: `uvicorn deployment.main:app --host 0.0.0.0 --port $PORT`
   - Environment: `USE_LIGHTWEIGHT_EMBEDDINGS=true`

### Option 2: Docker

```bash
cd deployment
docker build -t sahayak .
docker run -p 8000:8000 sahayak
```

### Option 3: Streamlit Cloud (Frontend only)

1. Deploy to https://share.streamlit.io
2. Add secrets:
   ```
   BACKEND_URL = "https://your-backend.onrender.com"
   ```

## Environment Variables:

- `USE_LIGHTWEIGHT_EMBEDDINGS=true` - Use hash-based embeddings (low memory)
- `USE_LIGHTWEIGHT_EMBEDDINGS=false` - Use ML embeddings (requires 2GB+ RAM)
- `COSDATA_URL` - Cosdata server URL
- `COSDATA_API_KEY` - Cosdata admin key

## Memory Requirements:

- **Lightweight**: ~100MB RAM (free tier compatible)
- **Full ML**: ~600MB RAM (needs paid tier)

## Notes:

- Free tiers use lightweight embeddings
- For production ML, use HuggingFace Inference API
- Cosdata automatically falls back to in-memory storage

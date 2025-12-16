# 🚀 FREE DEPLOYMENT GUIDE

## Option 1: Render + Streamlit Cloud ⭐ RECOMMENDED

### Step 1: Deploy Backend on Render.com

1. **Sign up at [render.com](https://render.com)** (free)

2. **Create New Web Service:**
   - Connect your GitHub repo: `Shikher-jain/Sahayak_09_02`
   - Name: `sahayak-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

3. **Your backend URL will be:** `https://sahayak-backend.onrender.com`

### Step 2: Deploy Frontend on Streamlit Cloud

1. **Sign up at [streamlit.io/cloud](https://streamlit.io/cloud)** (free)

2. **Create New App:**
   - Repository: `Shikher-jain/Sahayak_09_02`
   - Branch: `main`
   - Main file path: `frontend/app.py`

3. **Add Environment Variable:**
   - Key: `BACKEND_URL`
   - Value: `https://sahayak-backend.onrender.com` (your Render URL)

4. **Your app will be at:** `https://sahayak-shikher-jain.streamlit.app`

---

## Option 2: Railway.app (All-in-One) 🚂

1. **Sign up at [railway.app](https://railway.app)** (free $5/month credit)

2. **Deploy from GitHub:**
   - Connect repo: `Shikher-jain/Sahayak_09_02`
   - Railway auto-detects Python
   - Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

3. **For frontend (separate service):**
   - Create new service from same repo
   - Start command: `streamlit run frontend/app.py --server.port $PORT`

---

## Option 3: Hugging Face Spaces 🤗

1. **Sign up at [huggingface.co](https://huggingface.co)** (free)

2. **Create New Space:**
   - Space type: `Streamlit`
   - Upload your code
   - Add `requirements.txt` and `packages.txt`

3. **Automatic deployment!**

---

## ⚠️ Important Notes

### Cosdata Database:
- Free tiers don't support running Cosdata server
- **Solution:** Your code automatically falls back to **in-memory storage**
- Works perfectly for demo/testing
- For production, consider:
  - Self-hosted VPS (DigitalOcean $6/month)
  - Or use Qdrant Cloud (free tier available)

### OCR (Tesseract):
- ✅ Render: Install via `apt-packages.txt`
- ✅ Streamlit Cloud: Install via `packages.txt`
- ✅ Railway: Install in Dockerfile

### Free Tier Limitations:
| Platform | Pros | Cons |
|----------|------|------|
| **Render** | Easy, reliable | Sleeps after 15 min |
| **Streamlit Cloud** | Perfect for Streamlit | Frontend only |
| **Railway** | $5/month credit | Credit-based |
| **Hugging Face** | Always on, ML-friendly | Slower |

---

## 📋 Quick Deploy Checklist

- [x] `render.yaml` created
- [x] `packages.txt` created (for Tesseract)
- [x] `.streamlit/config.toml` created
- [x] Frontend updated to use `BACKEND_URL` env var
- [ ] Push to GitHub
- [ ] Deploy backend on Render
- [ ] Deploy frontend on Streamlit Cloud
- [ ] Set `BACKEND_URL` in Streamlit Cloud
- [ ] Test!

---

## 🎯 Recommended Setup (FREE!)

```
Frontend: Streamlit Cloud (FREE, always on)
    ↓ HTTP
Backend: Render.com (FREE, 750 hrs/month)
    ↓
Vector DB: In-memory fallback (included in code)
```

**Cost:** $0/month 🎉

---

## 🚀 Deploy Now!

### 1. Push your code:
```bash
git add .
git commit -m "Add deployment configs"
git push
```

### 2. Deploy Backend:
- Go to [dashboard.render.com](https://dashboard.render.com)
- New → Web Service
- Connect GitHub → Select your repo
- Deploy!

### 3. Deploy Frontend:
- Go to [streamlit.io/cloud](https://share.streamlit.io)
- New app → Select your repo
- Set `BACKEND_URL` in secrets
- Deploy!

### 4. Done! 🎉

Your app is now live and FREE!

---

## 💡 Pro Tips

1. **Keep it awake (Render):**
   - Use UptimeRobot (free) to ping every 5 min
   - Prevents cold starts

2. **Optimize for free tier:**
   - Reduce embedding model size if needed
   - Limit concurrent uploads
   - Add request caching

3. **Monitor usage:**
   - Check Render dashboard for hours used
   - Streamlit Cloud has no limits!

---

## 🔄 Alternative Vector Databases (Free Tiers)

If you want persistent vector storage:

1. **Qdrant Cloud** - 1GB free
   - Sign up at [cloud.qdrant.io](https://cloud.qdrant.io)
   - Get API key
   - Update `backend/db.py` to use Qdrant client

2. **Pinecone** - Free tier available
   - 100K vectors free
   - Easy to integrate

3. **Weaviate Cloud** - Sandbox available
   - 14 days free sandbox
   - Good for testing

---

Need help with deployment? Just ask! 🚀

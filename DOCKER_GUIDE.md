# 🐳 Docker Setup Guide

Run the entire Sahayak application with Docker - no local installations needed!

## 🚀 Quick Start

**Start all services (one command):**
```bash
docker-compose up --build
```

**Access the application:**
- Frontend UI: http://localhost:8501
- Backend API: http://localhost:8000
- Cosdata DB: http://localhost:8443

**Stop all services:**
```bash
docker-compose down
```

---

## 📦 What's Running?

### 1. Cosdata (Vector Database)
- Container: `sahayak-cosdata`
- Port: `8443`
- Image: `cosdata/cosdata:latest`
- Volume: Persistent storage for vectors
- Admin Key: `admin123` (change in docker-compose.yml)

### 2. Backend (FastAPI)
- Container: `sahayak-backend`
- Port: `8000`
- Built from: `Dockerfile`
- Features: PDF/OCR processing, embeddings, RAG
- Waits for Cosdata to be healthy before starting

### 3. Frontend (Streamlit)
- Container: `sahayak-frontend`
- Port: `8501`
- Built from: `Dockerfile.frontend`
- User interface for document upload and Q&A

---

## 🔧 Configuration

All configuration is in `docker-compose.yml`:

```yaml
environment:
  - COSDATA_URL=http://cosdata:8443
  - COSDATA_ADMIN_KEY=admin123
```

**To change the admin key:**
1. Edit `docker-compose.yml`
2. Update `COSDATA_ADMIN_KEY` in both `cosdata` and `backend` services
3. Restart: `docker-compose down && docker-compose up --build`

---

## 🛠️ Useful Commands

**View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f cosdata
docker-compose logs -f frontend
```

**Rebuild specific service:**
```bash
docker-compose up --build backend
```

**Restart a service:**
```bash
docker-compose restart backend
```

**Check service status:**
```bash
docker-compose ps
```

**Clean everything (including volumes):**
```bash
docker-compose down -v
```

---

## 📊 Health Checks

**Backend API health:**
```bash
curl http://localhost:8000/health
```

**Cosdata health:**
```bash
curl http://localhost:8443/health
```

---

## 🔍 Troubleshooting

### Port already in use
```bash
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :8443
netstat -ano | findstr :8501

# Kill the process or change ports in docker-compose.yml
```

### Container won't start
```bash
# Check logs
docker-compose logs backend

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Cosdata connection error
```bash
# Verify Cosdata is healthy
docker-compose ps

# Check Cosdata logs
docker-compose logs cosdata

# Restart Cosdata
docker-compose restart cosdata
```

### Data persistence
Data is stored in Docker volumes:
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect sahayak_09_02_cosdata_data
```

---

## 🚀 Production Deployment

For production, update `docker-compose.yml`:

1. **Change admin key:**
   ```yaml
   environment:
     - COSDATA_ADMIN_KEY=your-secure-key-here
   ```

2. **Add resource limits:**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 4G
   ```

3. **Use production-ready image tags:**
   ```yaml
   image: cosdata/cosdata:v1.0.0  # specific version
   ```

---

## 📝 File Structure

```
.
├── docker-compose.yml      # Orchestrates all services
├── Dockerfile              # Backend container
├── Dockerfile.frontend     # Frontend container
├── backend/               # FastAPI application
├── frontend/              # Streamlit application
└── data/                  # Uploaded files (mounted as volume)
```

---

## ✅ Advantages of Docker Setup

- ✅ No local Python/Tesseract/dependencies needed
- ✅ Consistent environment across machines
- ✅ Easy deployment to cloud platforms
- ✅ Isolated services with networking
- ✅ One command to start everything
- ✅ Perfect OS-agnostic solution (no Windows/Linux binary issues!)

---

## 🌐 Deploy to Cloud

### Docker Compose compatible platforms:
- **Railway**: `railway up`
- **Render**: Use Docker Compose support
- **DigitalOcean App Platform**: Docker Compose deployment
- **AWS ECS/Fargate**: Use docker-compose.yml
- **Google Cloud Run**: Multi-container support

---

**Questions? Check the logs first:**
```bash
docker-compose logs -f
```

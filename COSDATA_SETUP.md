# 🦁 Cosdata Database Setup Guide

Sahayak uses **Cosdata OSS**, a high-performance **vector database** for semantic search.  
Follow these steps to install and run the Cosdata server locally.

---

## 1. 🔧 Install Cosdata

### **Windows (Docker - Recommended)**

**Start Docker Desktop first**, then:

```powershell
# Pull the latest Cosdata image
docker pull cosdataio/cosdata:latest

# Run Cosdata server
docker run -d `
  --name cosdata-server `
  -p 8443:8443 `
  -p 50051:50051 `
  cosdataio/cosdata:latest

# Verify it's running
docker ps | Select-String "cosdata"
```

### **Linux / macOS (Native Binary)**

```bash
# Install Cosdata
curl -sL https://cosdata.io/install.sh | bash

# Set admin key
export COSDATA_ADMIN_KEY="admin123"

# Start server (keep this terminal open)
start-cosdata
```

### **Windows (WSL2)**

Open WSL terminal and follow the **Linux/macOS** instructions above.

---

## 2. 🚀 Start the Server

Open a **new terminal window** and run the server.
Keep this terminal open while using the app.

---

### **Linux / macOS (Native Binary)**

Navigate to the directory where Cosdata was installed:

```bash
start-cosdata
```

**Enter/Set Admin Key**

* `Admin Key:` (set your admin password)

---

### **Windows (Docker)**

If not already running, start the container:

```powershell
docker start cosdata-server
```

---

## 3. 🩺 Verify the Server

Run the health check:

```bash
curl http://127.0.0.1:8443/health
```

Expected output:

```json
{"status":"ok"}
```

This confirms the server is up and running.

---

## 4. 🛠️ Troubleshooting

### **❌ "Connection Refused" or "Database Full" Errors**

This happens if you restart the app repeatedly or the database becomes corrupted.

Follow these steps:

#### 1️⃣ Stop the server

**Docker:**
```powershell
docker stop cosdata-server
```

**Native:**
Press **Ctrl + C** in the server terminal.

#### 2️⃣ Delete existing Cosdata data

**Docker:**
```powershell
docker rm -f cosdata-server
docker volume prune -f
```

**Native:**
```bash
rm -rf data cosdata_data
```

#### 3️⃣ Restart the server

Follow the startup instructions above.

---

## 5. 🔧 Configuration

The backend connects to Cosdata using these default settings:

- **Host:** `http://127.0.0.1:8443`
- **Username:** `admin`
- **Password:** `admin`

You can modify these in your environment variables or backend configuration.

---

## 6. 📦 Managing Docker Container (Windows)

**View logs:**
```powershell
docker logs -f cosdata-server
```

**Stop server:**
```powershell
docker stop cosdata-server
```

**Remove container:**
```powershell
docker rm -f cosdata-server
```

**Persistent data volume (optional):**
```powershell
docker volume create cosdata-data

docker run -d `
  --name cosdata-server `
  -p 8443:8443 `
  -p 50051:50051 `
  -v cosdata-data:/root/.cosdata `
  cosdataio/cosdata:latest
```

---

## 📚 Additional Resources

- [Cosdata GitHub](https://github.com/cosdata/cosdata)
- [Cosdata Documentation](https://docs.cosdata.io/)
- [Docker Documentation](https://docs.docker.com/)

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.extractor import *
from backend.rag_engine import answer_question
from backend.embedder import embed_text
from backend.db import add_chunk, init_db, get_client
import os

# Use absolute path for compatibility
PDF_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "pdf_storage")
os.makedirs(PDF_FOLDER, exist_ok=True)

app = FastAPI(title="Sahayak - AI Teaching Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cosdata on startup
print("\n" + "="*60)
print("🚀 Initializing Sahayak AI Teaching Assistant")
print("="*60)
init_db()
print("="*60 + "\n")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload PDF/Image → Extract text → Generate embeddings → Store in Cosdata"""
    content = await file.read()
    try:
        filename = file.filename
        save_path = os.path.join(PDF_FOLDER, filename)
        print(f"\n📄 Processing: {filename}")
        # Save file locally
        with open(save_path, "wb") as f:
            f.write(content)
        print(f"  ✓ Saved to {save_path}")
        # Extract text based on file type
        if filename.lower().endswith(".pdf"):
            text = extract_pdf(content)
            print(f"  ✓ Extracted {len(text)} characters from PDF")
        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
            text = extract_image(content)
            print(f"  ✓ OCR extracted {len(text)} characters from image")
        else:
            return {"error": "Unsupported file type. Please upload PDF or image (PNG/JPG)"}
        if not text.strip():
            return {"error": "No text could be extracted from the file"}
        # Split into chunks (larger chunks for better context)
        chunk_size = 800
        overlap = 100
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i+chunk_size].strip()
            if chunk:
                chunks.append(chunk)
        print(f"  ✓ Split into {len(chunks)} chunks")
        # Generate embeddings and store in Cosdata
        fallback_used = False
        for idx, chunk in enumerate(chunks):
            emb = embed_text(chunk)
            # add_chunk does not return fallback status, so call add_vectors directly
            client = get_client()
            used_fallback = client.add_vectors([emb.tolist()], [{"filename": filename, "text": chunk}])
            if used_fallback:
                fallback_used = True
        if fallback_used:
            print(f"  ⚠ Cosdata unavailable, used in-memory fallback for this upload.")
        else:
            print(f"  ✓ Stored in Cosdata Vector DB\n")
        return {
            "message": f"✓ {filename} uploaded successfully!",
            "details": {
                "filename": filename,
                "text_length": len(text),
                "chunks_created": len(chunks),
                "cosdata_fallback": fallback_used
            },
            "warning": "Cosdata unavailable, used in-memory fallback. Data is not persistent." if fallback_used else None
        }
    except Exception as e:
        print(f"  ✗ Error: {str(e)}\n")
        return {"error": f"Processing failed: {str(e)}"}
    
@app.get("/cosdata_health")
def cosdata_health():
    """Check Cosdata vector DB health from backend"""
    client = get_client()
    healthy = client.health()
    return {"cosdata_healthy": healthy}

@app.get("/ask")
def ask(question: str):
    """Query documents using RAG with Cosdata vector search"""
    try:
        print(f"\n❓ Question: {question}")
        answer = answer_question(question)
        print(f"✓ Answer generated\n")
        return {"answer": answer}
    except Exception as e:
        print(f"✗ Error: {str(e)}\n")
        return {"error": str(e)}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Sahayak API is running"}

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Sahayak AI Teaching Assistant API",
        "endpoints": {
            "/upload": "POST - Upload PDF/Image files",
            "/ask": "GET - Ask questions about uploaded documents",
            "/health": "GET - Health check"
        }
    }

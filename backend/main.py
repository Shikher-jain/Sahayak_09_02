from fastapi import FastAPI, UploadFile
from backend.extractor import *
from backend.rag_engine import answer_question
from backend.embedder import embed_text
from backend.db import add_chunk, init_db

import os

PDF_FOLDER = os.path.join("..", "data", "pdf_storage")
os.makedirs(PDF_FOLDER, exist_ok=True)
app = FastAPI()
init_db()
@app.post("/upload")
async def upload_file(file: UploadFile):
    content = await file.read()
    try:
        filename = file.filename
        save_path = os.path.join(PDF_FOLDER, filename)
        # Save file locally
        with open(save_path, "wb") as f:
            f.write(content)

        # Extract text
        if filename.endswith(".pdf"):
            text = extract_pdf(content)
        elif filename.lower().endswith((".png", ".jpg")):
            text = extract_image(content)
        else:
            return {"error": "Unsupported file type"}

        # Split into chunks
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        for c in chunks:
            emb = embed_text(c)
            add_chunk(filename, c, emb)

        return {"message": f"{filename} uploaded and processed successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/ask")
def ask(question: str):
    try:
        answer = answer_question(question)  
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

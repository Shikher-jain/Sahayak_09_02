from backend.embedder import embed_text
from backend.db import search_similar_chunks
import numpy as np

def answer_question(question, top_k=5):
    try:
        query_vec = embed_text(question)
        
        # Search using Cosdata
        retrieved_chunks, scores = search_similar_chunks(query_vec, top_k)
        
        if not retrieved_chunks:
            return "No documents uploaded yet. Please upload PDF/image files first."
        
        # Filter out empty chunks
        retrieved_chunks = [chunk for chunk in retrieved_chunks if chunk.strip()]
        
        if not retrieved_chunks:
            return "No relevant information found in uploaded documents."
        
        # Build context from retrieved chunks
        context = "\n\n".join(retrieved_chunks)
        
        # For now, return the context as answer (you can integrate a local LLM later)
        response = f"""Based on the uploaded documents:

{context}

Relevant to your question: {question}"""
        
        return response
    except Exception as e:
        return f"Error processing question: {str(e)}"

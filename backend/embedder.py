import hashlib
import numpy as np

# Lightweight TF-IDF-like embeddings for deployment (no ML model needed)
# This is a fallback for memory-constrained environments
def embed_text(text):
    """
    Generate lightweight embeddings using character n-grams
    For production with ML, use HuggingFace Inference API or dedicated ML service
    """
    # Create 384-dim vector (compatible with MiniLM)
    vector = np.zeros(384)
    
    # Use text hash to generate pseudo-embedding
    text_lower = text.lower()
    words = text_lower.split()
    
    for i, word in enumerate(words[:384]):
        # Simple hash-based embedding
        hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16)
        vector[i % 384] += (hash_val % 1000) / 1000.0
    
    # Normalize
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm
    
    return vector

# For local development with full ML model (optional)
_use_ml = False
_model = None

def get_model():
    """Get or initialize the embedding model (only if ML enabled)"""
    global _model, _use_ml
    if _use_ml and _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            print("🔄 Loading ML embedding model...")
            _model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✓ Model loaded successfully")
        except ImportError:
            print("⚠️ sentence-transformers not available, using lightweight embeddings")
            _use_ml = False
    return _model

def embed_text_ml(text):
    """ML-based embedding (only for local/powerful servers)"""
    model = get_model()
    if model:
        return model.encode(text)
    return embed_text(text)

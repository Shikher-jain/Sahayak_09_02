from sentence_transformers import SentenceTransformer
import hashlib
import numpy as np
import os

# Check if we should use lightweight embeddings (for deployment)
USE_LIGHTWEIGHT = os.getenv("USE_LIGHTWEIGHT_EMBEDDINGS", "false").lower() == "true"

if not USE_LIGHTWEIGHT:
    # Full ML model (local development / powerful servers)
    _model = None

    def get_model():
        """Get or initialize the embedding model (lazy loading)"""
        global _model
        if _model is None:
            print("🔄 Loading embedding model...")
            _model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✓ Model loaded successfully")
        return _model

    def embed_text(text):
        """Generate embeddings using sentence-transformers"""
        model = get_model()
        return model.encode(text)
else:
    # Lightweight embeddings (deployment / memory-constrained)
    def embed_text(text):
        """Generate lightweight embeddings using hashing"""
        vector = np.zeros(384)
        text_lower = text.lower()
        words = text_lower.split()
        
        for i, word in enumerate(words[:384]):
            hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16)
            vector[i % 384] += (hash_val % 1000) / 1000.0
        
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector

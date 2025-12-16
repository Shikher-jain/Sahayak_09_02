from sentence_transformers import SentenceTransformer
import numpy as np

# ============================================================================
# LOCAL DEVELOPMENT (DEFAULT) - Uses ML model
# ============================================================================

# Lazy loading - model loaded ONLY on first use
_model = None

def get_model():
    """Get or initialize the embedding model (lazy loading)"""
    global _model
    if _model is None:
        print("🔄 Loading embedding model (first time only)...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Model loaded successfully")
    return _model

def embed_text(text):
    """Generate embeddings for text using lazy-loaded model"""
    model = get_model()
    return model.encode(text)


# ============================================================================
# DEPLOYMENT VERSION (Comment out above, uncomment below for Render/Heroku)
# ============================================================================
"""
import hashlib
import numpy as np

# Lightweight embeddings for memory-constrained deployments
def embed_text(text):
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
"""

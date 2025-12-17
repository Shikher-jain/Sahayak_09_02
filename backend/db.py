import httpx
import numpy as np
import os
from typing import List, Tuple, Dict, Any
import time
import json

# Cosdata Configuration
COSDATA_URL = os.getenv("COSDATA_URL", "http://127.0.0.1:8443")
COSDATA_ADMIN_KEY = os.getenv("COSDATA_ADMIN_KEY", "admin123")
COLLECTION_NAME = "pdf_documents"
EMBED_DIM = 384  # for 'all-MiniLM-L6-v2'

# In-memory fallback storage when COSDATA HTTP API is not fully available
_memory_vectors = []
_memory_metadata = []

class CosdataClient:
    """Client for Cosdata Vector Database"""
    
    def __init__(self):
        self.base_url = COSDATA_URL
        self.admin_key = COSDATA_ADMIN_KEY
        self.collection_name = COLLECTION_NAME
        self.headers = {
            "Content-Type": "application/json",
            "X-Admin-Key": self.admin_key
        }
        self.client = httpx.Client(timeout=180.0)
        
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make HTTP request to Cosdata"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.client.request(method, url, headers=self.headers, **kwargs)
            if response.status_code in [200, 201]:
                return response.json() if response.text else {}
            elif response.status_code == 404:
                return None
            else:
                print(f"Cosdata API returned status {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"[Cosdata] Request error: {e} (falling back to in-memory storage)")
            return None
        def health(self) -> bool:
            """Check if Cosdata is reachable and collection exists"""
            try:
                result = self._request("GET", f"/api/v1/collections/{self.collection_name}")
                if result is not None:
                    return True
            except Exception:
                pass
            return False
    
    def create_collection(self):
        """Create or verify collection exists"""
        try:
            # Try multiple API endpoints for collection creation
            endpoints = [
                "/api/v1/collections",
                "/collections",
                f"/collections/{self.collection_name}"
            ]
            
            payload = {
                "name": self.collection_name,
                "dimension": EMBED_DIM,
                "distance_metric": "cosine",
                "distance": "cosine"  # Alternative key name
            }
            
            for endpoint in endpoints:
                result = self._request("POST", endpoint, json=payload)
                if result is not None:
                    print(f"✓ Created Cosdata collection '{self.collection_name}' using {endpoint}")
                    return
            
            # If all fail, try PUT method
            result = self._request("PUT", f"/collections/{self.collection_name}", json=payload)
            if result is not None:
                print(f"✓ Created Cosdata collection '{self.collection_name}' using PUT")
            else:
                print(f"⚠ Could not create collection via API, will use in-memory fallback")
        except Exception as e:
            print(f"Collection setup error: {e}")
    
    def add_vectors(self, vectors: List[List[float]], metadata: List[dict]):
        """Add vectors with metadata to Cosdata collection"""
        global _memory_vectors, _memory_metadata
        used_fallback = False
        try:
            # Try COSDATA HTTP API first
            vector_data = []
            for i, (vec, meta) in enumerate(zip(vectors, metadata)):
                vector_data.append({
                    "id": f"{int(time.time() * 1000000)}_{i}",
                    "vector": vec,
                    "metadata": meta
                })
            payload = {"vectors": vector_data}
            result = self._request(
                "POST",
                f"/api/v1/collections/{self.collection_name}/vectors",
                json=payload
            )
            if result is not None:
                print(f"✓ Added {len(vectors)} vectors to Cosdata")
                return False  # Not using fallback
        except Exception as e:
            used_fallback = True
        # Fallback to in-memory storage
        for vec, meta in zip(vectors, metadata):
            _memory_vectors.append(vec)
            _memory_metadata.append(meta)
        print(f"[Fallback] Added {len(vectors)} vectors to in-memory storage (total: {len(_memory_vectors)})")
        return True  # Used fallback
    
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors in Cosdata"""
        global _memory_vectors, _memory_metadata
        
        try:
            # Try COSDATA HTTP API first
            payload = {
                "vector": query_vector,
                "k": top_k
            }
            
            result = self._request(
                "POST",
                f"/api/v1/collections/{self.collection_name}/search",
                json=payload
            )
            
            if result and "results" in result:
                return result["results"]
        except Exception as e:
            pass
        
        # Fallback to in-memory similarity search
        if not _memory_vectors:
            print("⚠ No vectors in memory storage")
            return []
        
        # Compute cosine similarity
        query_np = np.array(query_vector)
        similarities = []
        for i, vec in enumerate(_memory_vectors):
            vec_np = np.array(vec)
            similarity = np.dot(query_np, vec_np) / (np.linalg.norm(query_np) * np.linalg.norm(vec_np))
            similarities.append((i, similarity))
        
        # Sort and get top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_results = similarities[:top_k]
        
        # Format results
        results = []
        for idx, score in top_results:
            results.append({
                "metadata": _memory_metadata[idx],
                "score": float(score)
            })
        
        print(f"✓ Found {len(results)} results from in-memory storage")
        return results
    
    def delete_collection(self):
        """Delete the collection from Cosdata"""
        try:
            self._request("DELETE", f"/api/v1/collections/{self.collection_name}")
            print(f"✓ Deleted Cosdata collection '{self.collection_name}'")
        except Exception as e:
            print(f"Error deleting collection: {e}")
    
    def __del__(self):
        """Cleanup"""
        try:
            self.client.close()
        except:
            pass

# Global client instance
_client = None

def get_client():
    """Get or create Cosdata client"""
    global _client
    if _client is None:
        _client = CosdataClient()
    return _client

# Initialize database (create collection)
def init_db():
    """Initialize Cosdata collection"""
    client = get_client()
    client.create_collection()

# Add chunk with embedding
def add_chunk(filename: str, chunk_text: str, embedding: np.ndarray):
    """Add a document chunk to Cosdata"""
    client = get_client()
    
    # Convert numpy array to list
    vector = embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
    
    metadata = {
        "filename": filename,
        "text": chunk_text
    }
    
    client.add_vectors([vector], [metadata])

# Search for similar chunks
def search_similar_chunks(query_embedding: np.ndarray, top_k: int = 5) -> Tuple[List[str], List[float]]:
    """Search for similar document chunks"""
    client = get_client()
    
    # Convert numpy array to list
    query_vector = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
    
    results = client.search(query_vector, top_k)
    
    texts = []
    scores = []
    
    for result in results:
        metadata = result.get("metadata", {})
        texts.append(metadata.get("text", ""))
        scores.append(result.get("score", 0.0))
    
    return texts, scores


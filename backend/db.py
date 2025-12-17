import httpx
import numpy as np
import os
from typing import List, Tuple, Dict, Any
import time
import json
import platform

# Cosdata Configuration
# Windows Docker requires host.docker.internal, Linux uses localhost
DEFAULT_URL = "http://host.docker.internal:8443" if platform.system() == "Windows" else "http://127.0.0.1:8443"
COSDATA_URL = os.getenv("COSDATA_URL", DEFAULT_URL)
COSDATA_ADMIN_KEY = os.getenv("COSDATA_ADMIN_KEY", "admin123")
COLLECTION_NAME = "pdf_documents"
EMBED_DIM = 384  # for 'all-MiniLM-L6-v2'

class CosdataClient:
    """Client for Cosdata Vector Database - STRICT MODE (no silent fallbacks)"""
    
    def __init__(self):
        self.base_url = COSDATA_URL
        self.admin_key = COSDATA_ADMIN_KEY
        self.collection_name = COLLECTION_NAME
        self.headers = {
            "Content-Type": "application/json",
            "X-Admin-Key": self.admin_key
        }
        # Persistent client with proper timeout
        self.client = httpx.Client(
            timeout=httpx.Timeout(30.0, connect=10.0),
            follow_redirects=True
        )
        self._initialized = False
        
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make HTTP request to Cosdata - FAIL FAST on errors"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.client.request(method, url, headers=self.headers, **kwargs)
            if response.status_code in [200, 201]:
                return response.json() if response.text else {"success": True}
            elif response.status_code == 404:
                return None
            else:
                raise RuntimeError(f"Cosdata API error {response.status_code}: {response.text}")
        except httpx.TimeoutException as e:
            raise RuntimeError(f"Cosdata timeout after 30s: {e}. Check if Cosdata is running on {self.base_url}")
        except httpx.ConnectError as e:
            raise RuntimeError(f"Cannot connect to Cosdata at {self.base_url}: {e}")
        except Exception as e:
            raise RuntimeError(f"Cosdata request failed: {e}")
    
    def ping(self) -> bool:
        """Check if Cosdata is reachable"""
        try:
            result = self._request("GET", "/health")
            return True
        except:
            return False
    
    def collection_exists(self) -> bool:
        """Check if collection exists"""
        try:
            result = self._request("GET", f"/api/v1/collections/{self.collection_name}")
            return result is not None
        except:
            return False
    
    def create_collection(self):
        """Create collection - FAIL FAST if not possible"""
        if self._initialized:
            return
        
        # Check if already exists
        if self.collection_exists():
            print(f"✓ Cosdata collection '{self.collection_name}' already exists")
            self._initialized = True
            return
        
        # Try to create
        payload = {
            "name": self.collection_name,
            "dimension": EMBED_DIM,
            "distance_metric": "cosine",
            "distance": "cosine"  # Alternative key name
        }
        
        # Try multiple endpoints
        endpoints = [
            "/api/v1/collections",
            "/collections",
            f"/collections/{self.collection_name}"
        ]
        
        last_error = None
        for endpoint in endpoints:
            try:
                result = self._request("POST", endpoint, json=payload)
                if result is not None:
                    print(f"✓ Created Cosdata collection '{self.collection_name}' at {endpoint}")
                    self._initialized = True
                    return
            except Exception as e:
                last_error = e
                continue
        
        # All failed
        raise RuntimeError(
            f"Failed to create Cosdata collection '{self.collection_name}'. "
            f"Last error: {last_error}. Is Cosdata running at {self.base_url}?"
        )
    
    def add_vectors(self, vectors: List[List[float]], metadata: List[dict]):
        """Add vectors to Cosdata - NO FALLBACK"""
        if not self._initialized:
            raise RuntimeError("Cosdata not initialized. Call create_collection() first.")
        
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
        
        if result is None:
            raise RuntimeError("Failed to add vectors to Cosdata")
        
        print(f"✓ Added {len(vectors)} vectors to Cosdata")
    
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors in Cosdata - NO FALLBACK"""
        if not self._initialized:
            raise RuntimeError("Cosdata not initialized. Call create_collection() first.")
        
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
            print(f"✓ Found {len(result['results'])} results from Cosdata")
            return result["results"]
        
        # If no results key, return empty
        return []
    
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
    """Initialize Cosdata collection - FAIL FAST if Cosdata unavailable"""
    client = get_client()
    
    # 1. Check if Cosdata is reachable
    print(f"🔍 Checking Cosdata at {client.base_url}...")
    if not client.ping():
        raise RuntimeError(
            f"❌ Cosdata is NOT reachable at {client.base_url}\n"
            f"   → On Windows: Use 'host.docker.internal:8443'\n"
            f"   → Check: docker ps | grep cosdata\n"
            f"   → Cannot proceed without Cosdata."
        )
    print(f"✓ Cosdata is reachable")
    
    # 2. Create or verify collection
    client.create_collection()
    print(f"✓ Cosdata ready for vector operations")

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


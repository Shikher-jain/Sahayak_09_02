"""
Test script to verify Cosdata integration
"""
import sys
sys.path.append('.')

from backend.db import init_db, add_chunk, search_similar_chunks
from backend.embedder import embed_text
import numpy as np

def test_cosdata():
    print("=" * 60)
    print("Testing Cosdata Vector Database Integration")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing Cosdata collection...")
    init_db()
    
    # Add sample documents
    print("\n2. Adding sample documents...")
    samples = [
        ("What is machine learning?", "doc1.pdf"),
        ("Deep learning uses neural networks", "doc2.pdf"),
        ("Python is a programming language", "doc3.pdf"),
        ("Vector databases store embeddings", "doc4.pdf"),
        ("Cosdata is a vector database", "doc5.pdf")
    ]
    
    for text, filename in samples:
        embedding = embed_text(text)
        add_chunk(filename, text, embedding)
    
    print(f"✓ Added {len(samples)} documents")
    
    # Search for similar documents
    print("\n3. Testing search...")
    query = "Tell me about vector databases"
    print(f"Query: '{query}'")
    
    query_embedding = embed_text(query)
    results, scores = search_similar_chunks(query_embedding, top_k=3)
    
    print(f"\n✓ Found {len(results)} similar documents:")
    for i, (text, score) in enumerate(zip(results, scores), 1):
        print(f"   {i}. [Score: {score:.4f}] {text}")
    
    print("\n" + "=" * 60)
    print("✅ Cosdata integration test completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    test_cosdata()

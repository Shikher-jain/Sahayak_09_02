#!/usr/bin/env python3
"""
Test script for Sahayak AI Teaching Assistant
Tests the complete pipeline: Upload → Extract → Embed → Store → Query
"""

import requests
import sys
import os

BACKEND_URL = "http://localhost:8000"

def test_health():
    """Test if backend is running"""
    print("\n🔍 Testing backend health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Backend is running")
            return True
        else:
            print(f"✗ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend. Make sure it's running:")
        print("   cd backend && python -m uvicorn main:app --reload")
        return False

def test_upload(file_path):
    """Test file upload"""
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return False
        
    print(f"\n📤 Uploading file: {file_path}")
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                print(f"✗ Upload error: {result['error']}")
                return False
            else:
                print(f"✓ Upload successful")
                if 'details' in result:
                    details = result['details']
                    print(f"  - Chunks created: {details.get('chunks_created', 'N/A')}")
                    print(f"  - Text length: {details.get('text_length', 'N/A')}")
                return True
        else:
            print(f"✗ Upload failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Upload error: {e}")
        return False

def test_query(question):
    """Test question answering"""
    print(f"\n❓ Asking: {question}")
    try:
        response = requests.get(
            f"{BACKEND_URL}/ask",
            params={"question": question},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                print(f"✗ Query error: {result['error']}")
                return False
            else:
                print(f"✓ Answer received:")
                print(f"\n{result.get('answer', 'No answer')}\n")
                return True
        else:
            print(f"✗ Query failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Query error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 Sahayak System Test")
    print("="*60)
    
    # Test 1: Health check
    if not test_health():
        sys.exit(1)
    
    # Test 2: Upload (if file provided)
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if not test_upload(file_path):
            print("\n⚠️  Upload failed, but continuing with query test...")
    else:
        print("\n⚠️  No file provided for upload test")
        print("   Usage: python test_system.py <pdf_file>")
    
    # Test 3: Query
    test_questions = [
        "What is this document about?",
        "Summarize the main points",
        "What are the key concepts?"
    ]
    
    print("\n" + "="*60)
    print("📝 Testing Queries")
    print("="*60)
    
    for question in test_questions:
        test_query(question)
    
    print("="*60)
    print("✓ Testing complete!")
    print("="*60)

if __name__ == "__main__":
    main()

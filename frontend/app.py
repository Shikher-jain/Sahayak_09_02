import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Sahayak - AI Teaching Assistant",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Sahayak - AI Teaching Assistant")
st.markdown("Upload PDFs or Images and ask questions about them!")

# Backend URL (localhost by default)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **Sahayak** uses:
    - 🧠 Semantic search (embeddings)
    - 📄 PDF text extraction
    - 🖼️ OCR for images
    - 💾 Cosdata Vector DB
    """)
    
    st.divider()
    
    # Check backend status
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ Backend connected")
        else:
            st.error("❌ Backend error")
    except:
        st.error("❌ Backend offline")
        st.info("Start backend:\n```\ncd backend\nuvicorn main:app --reload\n```")

# Main area
file = st.file_uploader("📎 Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
question = st.text_input("❓ Ask your question", placeholder="e.g., What is this document about?")

if file:
    with st.spinner("Uploading and processing..."):
        try:
            res = requests.post(f"{BACKEND_URL}/upload", files={"file": file}, timeout=120)
            response_data = res.json()
            
            if "error" in response_data:
                st.error(f"❌ {response_data['error']}")
            else:
                st.success(response_data.get("message", "File uploaded successfully"))
                
                # Show details if available
                if "details" in response_data:
                    details = response_data["details"]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Text Length", f"{details.get('text_length', 0):,}")
                    with col2:
                        st.metric("Chunks Created", details.get('chunks_created', 0))
                        
        except Exception as e:
            st.error(f"❌ Upload error: {str(e)}")

if st.button("🔍 Ask", use_container_width=True):
    if not question.strip():
        st.warning("⚠️ Please enter a question first!")
    else:
        with st.spinner("Searching for answer..."):
            try:
                res = requests.get(f"{BACKEND_URL}/ask", params={"question": question}, timeout=120)
                response_data = res.json()
                
                if "error" in response_data:
                    st.error(f"❌ {response_data['error']}")
                else:
                    st.markdown("### 💡 Answer:")
                    st.info(response_data.get("answer", "No answer received"))
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

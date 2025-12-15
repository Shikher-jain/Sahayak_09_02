import streamlit as st
import requests

st.title("📄 AI Teaching Assistant - Multi-PDF Memory")

file = st.file_uploader("Upload PDF/Image")
question = st.text_input("Ask your question")

BACKEND_URL = "http://localhost:8000"
# BACKEND_URL = "https://sahayak-09-02.onrender.com"  # Example for deployed backend

if file:
    try:
        res = requests.post(f"{BACKEND_URL}/upload", files={"file": file})

        response_data = res.json()
        if "error" in response_data:
            st.error(f"Upload failed: {response_data['error']}")
        else:
            st.success(response_data.get("message", "File uploaded successfully"))
    except Exception as e:
        st.error(f"Upload error: {str(e)}")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question first!")
    else:
        try:
            res = requests.get(f"{BACKEND_URL}/ask", params={"question": question})
            response_data = res.json()
            if "error" in response_data:
                st.error(f"Error: {response_data['error']}")
            else:
                st.write(response_data.get("answer", "No answer received"))
        except Exception as e:
            st.error(f"Error: {str(e)}")

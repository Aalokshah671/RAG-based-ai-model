import streamlit as st
from rag_qa import rag_answer, create_embedding, FAISS_INDEX_PATH, METADATA_PATH, index, metadata
import os
from PyPDF2 import PdfReader
import tempfile
import requests

st.set_page_config(page_title="RAG Chat Assistant", layout="centered")
st.title("🤖 RAG-based AI Teaching Assistant with PDF & Video")
st.caption("Upload PDFs or videos and ask questions from them")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize uploaded documents
if "docs" not in st.session_state:
    st.session_state.docs = []

# ---------------- PDF UPLOAD ----------------
uploaded_pdf = st.file_uploader("Choose PDF", type=["pdf"])
if uploaded_pdf:
    if st.button("Send to Backend"):
        with st.spinner("Uploading and processing PDF..."):
            files = {"file": (uploaded_pdf.name, uploaded_pdf, "application/pdf")}
            response = requests.post("http://127.0.0.1:8000/upload_pdf", files=files)
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(f"Failed: {response.text}")

# ---------------- VIDEO UPLOAD (extract subtitles or speech-to-text) ----------------
uploaded_video = st.file_uploader("Upload Video (mp4)", type=["mp4"])
if uploaded_video:
    with st.spinner("Processing Video..."):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_video.read())
        temp_file_path = temp_file.name
        # Here you can integrate a speech-to-text model like OpenAI Whisper
        st.session_state.docs.append("Video transcription goes here")
        st.success("Video uploaded! (Transcription placeholder)")

# ---------------- Display previous messages ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- Chat input ----------------
question = st.chat_input("Ask a question...")

if question:
    # Combine uploaded docs into context if any
    combined_context = "\n\n".join(st.session_state.docs)

    # Optionally, you can feed this combined_context to RAG retrieval before asking LLM
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if combined_context:
                    # If there is uploaded content, we can prepend it to RAG answer
                    answer = rag_answer(question)  # Existing RAG pipeline
                    answer = f"{answer}\n\n[Based on uploaded documents]"  # optional
                else:
                    answer = rag_answer(question)
            except Exception as e:
                answer = f"⚠️ Error: {e}"

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
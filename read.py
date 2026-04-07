# from fastapi import FastAPI, UploadFile, File
# from PyPDF2 import PdfReader
# import json
# import os

# app = FastAPI()

# UPLOAD_FOLDER = "data"
# OUTPUT_FOLDER = "output"

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# def read_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     text = ""

#     for page in reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"

#     return text


# @app.post("/upload_pdf")
# async def upload_pdf(file: UploadFile = File(...)):
    
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#     # ✅ Save uploaded file
#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     # ✅ Read PDF
#     pdf_text = read_pdf(file_path)

#     # ✅ Convert to JSON
#     pdf_json = {
#         "source_file": file.filename,
#         "language": "english",
#         "content": pdf_text
#     }

#     json_path = os.path.join(OUTPUT_FOLDER, "pdf_text.json")

#     # ✅ Save JSON
#     with open(json_path, "w", encoding="utf-8") as f:
#         json.dump(pdf_json, f, indent=4, ensure_ascii=False)

#     return {"message": "PDF uploaded and processed successfully ✅"}




from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
import os
import json
import numpy as np
import faiss
import requests

app = FastAPI()

UPLOAD_FOLDER = "data"
OUTPUT_FOLDER = "output"
CHUNK_FOLDER = "chunking"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(CHUNK_FOLDER, exist_ok=True)

# ---------------- PDF READ ----------------
def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


# ---------------- CHUNKING (YOUR LOGIC SAME) ----------------
def chunk_text(text, source, doc_type, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    chunk_id = 1

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append({
            "chunk_id": f"{source}_{chunk_id}",
            "source": source,
            "type": doc_type,
            "content": chunk,
            "start_char": start,
            "end_char": end
        })

        chunk_id += 1
        start = end - overlap

    return chunks


# ---------------- EMBEDDING (UNCHANGED) ----------------
def create_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "bge-m3", "prompt": text}
    )
    response.raise_for_status()
    return response.json()["embedding"]


# ---------------- API ----------------
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):

    # 1. Save PDF
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2. Extract text
    pdf_text = read_pdf(file_path)

    # 3. Convert to same JSON format (like your old file)
    doc_json = {
        "source": file.filename,
        "type": "pdf",
        "content": pdf_text
    }

    # 4. Chunking (YOUR SAME FORMAT)
    chunks = chunk_text(
        doc_json["content"],
        doc_json["source"],
        doc_json["type"]
    )

    # Save chunks
    chunk_file = os.path.join(CHUNK_FOLDER, "chunks.json")
    with open(chunk_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

    # 5. Embeddings (UNCHANGED)
    texts = [chunk["content"] for chunk in chunks]
    embeddings = [create_embedding(text) for text in texts]

    embeddings = np.array(embeddings).astype("float32")

    # 6. FAISS
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, os.path.join(OUTPUT_FOLDER, "vector_index.faiss"))

    # 7. Save metadata
    with open(os.path.join(OUTPUT_FOLDER, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

    return {
        "message": "✅ PDF → Chunk → Embedding → FAISS DONE",
        "total_chunks": len(chunks)
    }
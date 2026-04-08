import requests
import json
import faiss
import numpy as np
import os

# -----------------------------
# CONFIG
# -----------------------------
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "bge-m3"
LLM_MODEL = "llama3"

FAISS_INDEX_PATH = "output/vector_index.faiss"
METADATA_PATH = "output/metadata.json"
TOP_K = 3


# -----------------------------
# CREATE EMBEDDING
# -----------------------------
def create_embedding(text: str) -> np.ndarray:
    payload = {
        "model": EMBED_MODEL,
        "prompt": text
    }

    r = requests.post(f"{OLLAMA_URL}/api/embeddings", json=payload)
    r.raise_for_status()

    return np.array(r.json()["embedding"], dtype="float32")


# -----------------------------
# LOAD FAISS + METADATA
# -----------------------------
# def load_faiss():
#     if not os.path.exists(FAISS_INDEX_PATH):
#         raise FileNotFoundError("❌ FAISS index not found")

#     if not os.path.exists(METADATA_PATH):
#         raise FileNotFoundError("❌ metadata.json not found")

#     index = faiss.read_index(FAISS_INDEX_PATH)

#     with open(METADATA_PATH, "r", encoding="utf-8") as f:
#         metadata = json.load(f)

#     return index, metadata

def load_faiss():
    if not os.path.exists(FAISS_INDEX_PATH):
        print("⚠️ FAISS index not found, upload PDF first")
        return None, None

    index = faiss.read_index(FAISS_INDEX_PATH)

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata


index, metadata = load_faiss()
if index is None or metadata is None:
    print("⚠️ No data available. Please upload PDF first.")

# -----------------------------
# RETRIEVE CONTEXT
# -----------------------------
def retrieve_context(question: str) -> str:
    query_vector = create_embedding(question).reshape(1, -1)

    distances, indices = index.search(query_vector, TOP_K)

    context_chunks = []
    for i in indices[0]:
        # 👇 IMPORTANT FIX (content key)
        context_chunks.append(metadata[i]["content"])

    return "\n\n".join(context_chunks)


# -----------------------------
# ASK LLM
# -----------------------------
def ask_llm(context: str, question: str) -> str:
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Answer ONLY from the given context. If answer is not in context, say 'Not found in context'."
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}
"""
            }
        ],
        "stream": False
    }

    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload)
    r.raise_for_status()

    return r.json()["message"]["content"]


# -----------------------------
# RAG PIPELINE
# -----------------------------
def rag_answer(question: str) -> str:
    context = retrieve_context(question)
    return ask_llm(context, question)


# -----------------------------
# CLI LOOP
# -----------------------------
if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'exit'): ")

        if q.lower() == "exit":
            break

        try:
            answer = rag_answer(q)
            print("\n🧠 Answer:\n", answer)
        except Exception as e:
            print("\n❌ Error:", e)

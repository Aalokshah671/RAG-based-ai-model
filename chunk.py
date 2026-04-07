import json
import os

# Settings
input_folder = "output"
output_folder = "chunking"
chunk_size = 500      # characters per chunk
overlap = 50          # overlapping characters
chunk_file = os.path.join(output_folder, "chunks7.json")

# ✅ Load all JSON files
documents = []
for file_name in ["audio_text.json"]:
    path = os.path.join(input_folder, file_name)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        documents.append(data)

# ✅ Function to create chunks
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

# ✅ Create chunks for all documents
# ✅ Create chunks for all documents
all_chunks = []
for doc in documents:
    source = doc.get("source", "unknown_source")
    doc_type = doc.get("type", "unknown_type")
    text = doc.get("content", "")
    all_chunks.extend(chunk_text(text, source, doc_type, chunk_size, overlap))

# ✅ Save chunks
with open(chunk_file, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=4, ensure_ascii=False)

# print(f"✅ Chunking completed. Total chunks: {len(all_chunks)}")
# print(f"📄 Saved at: {chunk_file}")

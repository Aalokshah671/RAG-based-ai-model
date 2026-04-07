import requests
import json
import numpy as np
import faiss

def create_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "bge-m3", "prompt": text}
    )
    response.raise_for_status()
    return response.json()["embedding"]

# Load chunks
with open("chunking/chunks6.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["content"] for chunk in chunks]

# Create embeddings
embeddings = [create_embedding(text) for text in texts]
embeddings = np.array(embeddings).astype("float32")

# FAISS
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, "output/vector_index.faiss")

# Save metadata
with open("output/metadata.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print("Ollama (bge-m3) embeddings + FAISS ready!")





# import requests
# import os
# import json

# def create_embedding(text_list):
#     # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
#     r = requests.post("http://localhost:11434/api/embed", json={
#         "model": "bge-m3",
#         "input": text_list
#     })

#     embedding = r.json()["embeddings"] 
#     return embedding


# jsons = os.listdir("jsons")  # List all the jsons 
# my_dicts = []
# chunk_id = 0

# for json_file in jsons:
#     with open(f"jsons/{json_file}") as f:
#         content = json.load(f)
#     print(f"Creating Embeddings for {json_file}")
#     embeddings = create_embedding([c['text'] for c in content['chunks']])
       
#     for i, chunk in enumerate(content['chunks']):
#         chunk['chunk_id'] = chunk_id
#         chunk['embedding'] = embeddings[i]
#         chunk_id += 1
#         my_dicts.append(chunk) 
# # print(my_dicts)

# df = pd.DataFrame.from_records(my_dicts)
# print(df)
# # a = create_embedding(["Cat sat on the mat", "Harry dances on a mat"])
# # print(a)
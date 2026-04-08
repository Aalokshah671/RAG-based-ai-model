import whisper
# model=whisper.load_model("large-v2")
# result=model.transcribe(audio="audios/1_brand.mp3",
#                         language="hi",
#                         task="translate")
# print(result["text"])


import json
import os

# Load model
model = whisper.load_model("large-v2")

# Transcribe + Translate
result = model.transcribe(
    audio="audios/1_brand.mp3",
    language="hi",
    task="translate"
)

# Extract text
text = result["text"]

# ✅ SAME folder jahan PDF JSON hai
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Create JSON
audio_json = {
    "source": "1_brand.mp3",
    "type": "audio",
    "language": "english",
    "content": text
}

# Save JSON
json_path = os.path.join(output_folder, "audio_text.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(audio_json, f, indent=4, ensure_ascii=False)

# print("✅ Speech converted and saved as JSON")
# print(f"📄 Saved at: {json_path}")

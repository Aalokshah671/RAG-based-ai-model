# from PyPDF2 import PdfReader

# pdf_path="data/sample_test_content.pdf"


# def read_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     text = ""

#     for page in reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"

#     return text


# # print(read_pdf)

# pdf_text = read_pdf(pdf_path)
# print(pdf_text)

from PyPDF2 import PdfReader
import json
import os

# app = FastAPI()

pdf_path = "data/llm.pdf"
output_folder = "output"

def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


# ✅ Read PDF
pdf_text = read_pdf(pdf_path)

# ✅ Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# ✅ Convert to JSON format
pdf_json = {
    "source_file": "data/llm.pdf",
    "language": "english",
    "content": pdf_text
}

# ✅ Save JSON file
json_path = os.path.join(output_folder, "3pdf_text.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(pdf_json, f, indent=4, ensure_ascii=False)

# print("✅ PDF read successfully")
# print("✅ Converted to JSON")
# print(f"📄 JSON saved at: {json_path}")


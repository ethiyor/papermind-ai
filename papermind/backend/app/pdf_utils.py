# app/pdf_utils.py
from io import BytesIO
from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_stream = BytesIO(file_bytes)
    text = extract_text(pdf_stream)
    return text

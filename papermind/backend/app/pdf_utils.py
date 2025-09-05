# app/pdf_utils.py
from io import BytesIO
from pdfminer.high_level import extract_text
import logging

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes with error handling"""
    try:
        pdf_stream = BytesIO(file_bytes)
        text = extract_text(pdf_stream)
        
        # Clean up the extracted text
        if text:
            # Remove excessive whitespace and normalize
            text = ' '.join(text.split())
            return text
        else:
            print("Warning: No text extracted from PDF")
            return ""
            
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

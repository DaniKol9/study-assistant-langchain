"""
Document loaders for the study assistant.

Currently supports PDF text extraction using PyPDF2.
"""

from PyPDF2 import PdfReader

def load_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    chunks = []
    for page in reader.pages:
        text = page.extract_text() or ""
        chunks.append(text)
    return "\n".join(chunks)
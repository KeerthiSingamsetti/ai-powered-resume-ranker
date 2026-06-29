"""
resume_parser.py
────────────────
Extracts raw text from PDF resumes.
Primary: pdfplumber (better table/layout handling)
Fallback: PyPDF2
"""

import io
import re
import pdfplumber
import PyPDF2


def extract_text_from_pdf(file) -> str:
    """
    Accept a file-like object (Streamlit UploadedFile or BytesIO) and
    return all extracted text as a single string.
    """
    # Read bytes once so we can seek multiple times
    if hasattr(file, "read"):
        raw_bytes = file.read()
    else:
        raw_bytes = file  # already bytes

    text = _extract_with_pdfplumber(raw_bytes)
    if not text or len(text.strip()) < 50:
        text = _extract_with_pypdf2(raw_bytes)

    return _clean_text(text)


def _extract_with_pdfplumber(raw_bytes: bytes) -> str:
    try:
        with pdfplumber.open(io.BytesIO(raw_bytes)) as pdf:
            pages = []
            for page in pdf.pages:
                pg_text = page.extract_text()
                if pg_text:
                    pages.append(pg_text)
            return "\n".join(pages)
    except Exception:
        return ""


def _extract_with_pypdf2(raw_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(raw_bytes))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages)
    except Exception:
        return ""


def _clean_text(text: str) -> str:
    """Remove excessive whitespace while keeping line structure."""
    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip trailing spaces on each line
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip()

import io
from pypdf import PdfReader


def extract_text(data: bytes) -> dict:
    """Takes raw PDF bytes, returns page count and the full text."""
    reader = PdfReader(io.BytesIO(data))

    if reader.is_encrypted:
        raise ValueError("This PDF is password-protected.")

    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    text = "\n\n".join(pages).strip()

    return {"pages": len(reader.pages), "text": text}
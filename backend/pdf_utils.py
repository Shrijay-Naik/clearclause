import io

from pypdf import PdfReader

MAX_PAGES = 100


def extract_text(data: bytes) -> dict:
    """Takes raw PDF bytes, returns page count and the full text."""
    reader = PdfReader(io.BytesIO(data))

    if reader.is_encrypted:
        raise ValueError("This PDF is password-protected.")

    if len(reader.pages) > MAX_PAGES:
        raise ValueError(
            f"This PDF has {len(reader.pages)} pages. The limit is {MAX_PAGES} pages."
        )

    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    text = "\n\n".join(pages).strip()

    return {"pages": len(reader.pages), "text": text}
from io import BytesIO
from typing import Iterable

from fastapi import HTTPException, status
from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF byte stream."""
    try:
        reader = PdfReader(BytesIO(file_bytes))
    except Exception as exc:  # pragma: no cover - defensive for corrupt PDFs
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read PDF: {exc}",
        ) from exc

    pages_text: Iterable[str] = (page.extract_text() or "" for page in reader.pages)
    combined_text = "\n".join(page_text.strip() for page_text in pages_text if page_text)

    if not combined_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF contains no extractable text.",
        )

    return combined_text



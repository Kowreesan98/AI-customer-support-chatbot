from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.services.pdf import extract_text_from_pdf
from app.services.vectorstore import vector_store_service

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_pdf(file: UploadFile = File(...)) -> dict[str, str | int]:
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF uploads are supported.",
        )

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    chunks_added = vector_store_service.add_text(text=text, source=file.filename)

    return {"status": "processed", "chunks_added": chunks_added, "filename": file.filename}



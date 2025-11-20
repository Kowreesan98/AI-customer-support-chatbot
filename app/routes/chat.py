from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.db import crud
from app.db.session import get_db
from app.services.llm import llm_service
from app.services.vectorstore import vector_store_service

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


class DocumentChunk(BaseModel):
    content: str
    source: str | None = None


class ChatResponse(BaseModel):
    answer: str
    context: List[DocumentChunk]


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db=Depends(get_db)) -> ChatResponse:
    documents = vector_store_service.similarity_search(request.question, k=3)
    context_strings = [doc.page_content for doc in documents]
    response_text = llm_service.generate_response(
        question=request.question, context_chunks=context_strings
    )

    crud.create_chat_log(
        session=db,
        question=request.question,
        response=response_text,
    )

    context = [
        DocumentChunk(content=doc.page_content, source=doc.metadata.get("source"))
        for doc in documents
    ]
    return ChatResponse(answer=response_text, context=context)



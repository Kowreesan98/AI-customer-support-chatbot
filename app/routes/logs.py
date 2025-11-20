from typing import List

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.db import crud
from app.db.session import get_db

router = APIRouter()


class ChatLogItem(BaseModel):
    question: str
    response: str
    created_at: str


@router.get("/", response_model=List[ChatLogItem])
async def get_logs(limit: int = Query(default=100, ge=1, le=500), db=Depends(get_db)):
    logs = crud.list_chat_logs(session=db, limit=limit)
    return [
        ChatLogItem(
            question=log.question,
            response=log.response,
            created_at=log.created_at.isoformat(),
        )
        for log in logs
    ]



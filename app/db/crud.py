from typing import Iterable, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import models


def create_chat_log(session: Session, *, question: str, response: str) -> models.ChatLog:
    chat_log = models.ChatLog(question=question, response=response)
    session.add(chat_log)
    session.flush()  # Ensure ID/timestamp assigned.
    return chat_log


def list_chat_logs(session: Session, limit: int = 100) -> List[models.ChatLog]:
    stmt = select(models.ChatLog).order_by(models.ChatLog.created_at.desc()).limit(limit)
    return list(session.execute(stmt).scalars().all())



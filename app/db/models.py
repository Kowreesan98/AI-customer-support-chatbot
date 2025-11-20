from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text

from app.db.session import Base


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)



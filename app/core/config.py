from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "AI Customer Support Chatbot"
    api_v1_prefix: str = ""
    openai_api_key: Optional[str] = None
    llm_provider: str = "openai"
    llm_model_name: str = "gpt-4o-mini"
    embedding_model_name: str = "text-embedding-3-small"
    faiss_index_path: Path = Path("data") / "faiss_index"
    sqlite_url: str = "sqlite:///data/chatlogs.db"
    cors_allow_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()



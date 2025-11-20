from typing import Iterable

from fastapi import HTTPException, status
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from app.core.config import get_settings

settings = get_settings()


def _build_llm() -> Runnable:
    provider = settings.llm_provider.lower()
    if provider == "openai":
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY environment variable is not set.",
            )
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            openai_api_key=settings.openai_api_key,
            model=settings.llm_model_name,
            temperature=0.2,
        )
    if provider == "ollama":
        from langchain_community.chat_models import ChatOllama

        return ChatOllama(model=settings.llm_model_name, temperature=0.2)

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Unsupported LLM provider '{settings.llm_provider}'.",
    )


class LLMService:
    """Orchestrate LLM prompts using LangChain."""

    def __init__(self) -> None:
        self._llm = _build_llm()
        self._prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are an AI customer support assistant. "
                        "Use the provided context to answer the user's question accurately. "
                        "If the answer is not contained in the context, say you don't know."
                    ),
                ),
                (
                    "human",
                    "Context:\n{context}\n\nQuestion: {question}",
                ),
            ]
        )

    def generate_response(self, *, question: str, context_chunks: Iterable[str]) -> str:
        context = "\n\n".join(context_chunks) or "No context provided."
        chain = self._prompt | self._llm

        try:
            response = chain.invoke({"question": question, "context": context})
        except Exception as exc:  # pragma: no cover - handles API errors.
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"LLM request failed: {exc}",
            ) from exc

        return response.content if hasattr(response, "content") else str(response)


llm_service = LLMService()



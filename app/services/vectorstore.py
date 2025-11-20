from pathlib import Path
from typing import List, Sequence

from fastapi import HTTPException, status
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from app.core.config import get_settings

settings = get_settings()
INDEX_PATH = Path(settings.faiss_index_path)


class VectorStoreService:
    """Manage persistent FAISS vector store with LangChain."""

    def __init__(self) -> None:
        self._vector_store: FAISS | None = None
        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    def _get_embeddings(self) -> OpenAIEmbeddings:
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY environment variable is not set.",
            )

        return OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key,
            model=settings.embedding_model_name,
        )

    def _ensure_loaded(self) -> None:
        if self._vector_store is None:
            if (INDEX_PATH / "index.faiss").exists():
                self._vector_store = FAISS.load_local(
                    INDEX_PATH,
                    self._get_embeddings(),
                    allow_dangerous_deserialization=False,
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No knowledge base found. Upload documents first.",
                )

    def _split_text(self, text: str) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=150, separators=["\n\n", "\n", ".", " "]
        )
        return splitter.create_documents([text])

    def add_text(self, *, text: str, source: str) -> int:
        documents = self._split_text(text)
        for doc in documents:
            doc.metadata["source"] = source

        if (INDEX_PATH / "index.faiss").exists():
            vector_store = FAISS.load_local(
                INDEX_PATH,
                self._get_embeddings(),
                allow_dangerous_deserialization=False,
            )
            vector_store.add_documents(documents)
        else:
            vector_store = FAISS.from_documents(documents, self._get_embeddings())

        vector_store.save_local(INDEX_PATH)
        self._vector_store = vector_store
        return len(documents)

    def similarity_search(self, query: str, k: int = 3) -> Sequence[Document]:
        self._ensure_loaded()
        assert self._vector_store  # For type checkers; _ensure_loaded handles errors.
        return self._vector_store.similarity_search(query, k=k)


vector_store_service = VectorStoreService()



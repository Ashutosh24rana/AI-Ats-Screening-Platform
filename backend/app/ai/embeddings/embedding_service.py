from functools import lru_cache

from langchain_core.embeddings import Embeddings

from app.core.config import settings


@lru_cache
def get_embedding_service() -> Embeddings:
    """Configurable embedding provider (defaults to Google Gemini embeddings)."""
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.llm_api_key,
    )


class EmbeddingService:
    def __init__(self, embeddings: Embeddings | None = None):
        self.embeddings = embeddings or get_embedding_service()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)

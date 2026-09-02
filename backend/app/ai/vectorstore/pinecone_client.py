from functools import lru_cache

from langchain_pinecone import PineconeVectorStore

from app.ai.chunking.resume_chunker import ResumeChunker
from app.ai.embeddings.embedding_service import get_embedding_service
from app.core.config import settings


def _ensure_index():
    from pinecone import Pinecone, ServerlessSpec

    client = Pinecone(api_key=settings.pinecone_api_key)
    existing = [index["name"] for index in client.list_indexes()]
    if settings.pinecone_index_name not in existing:
        embedding_dimensions = len(get_embedding_service().embed_query("dimension probe"))
        client.create_index(
            name=settings.pinecone_index_name,
            dimension=embedding_dimensions,
            metric="cosine",
            spec=ServerlessSpec(cloud=settings.pinecone_cloud, region=settings.pinecone_region),
        )
    return client.Index(settings.pinecone_index_name)


@lru_cache
def get_pinecone_index():
    return _ensure_index()


class ResumeVectorStore:
    """Stores and retrieves resume chunks in Pinecone with metadata filtering."""

    def __init__(self):
        self.vectorstore = PineconeVectorStore(index=get_pinecone_index(), embedding=get_embedding_service())

    def store_resume_chunks(self, chunks) -> list[str]:
        return self.vectorstore.add_documents(chunks)

    def chunk_and_store(self, resume_text: str, metadata: dict) -> list[str]:
        chunks = ResumeChunker().split(resume_text, metadata=metadata)
        return self.store_resume_chunks(chunks)

    def retrieve_for_candidate(self, query: str, job_id: str, candidate_id: str, top_k: int | None = None):
        """Retrieve relevant resume chunks filtered by the current job/candidate."""
        k = top_k or settings.retrieval_top_k
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k,
                "filter": {"job_id": {"$eq": job_id}, "candidate_id": {"$eq": candidate_id}},
            },
        )
        return retriever.invoke(query)

    @staticmethod
    def format_chunks(documents) -> str:
        parts = []
        for doc in documents:
            section = doc.metadata.get("section", "other")
            parts.append(f"[{section}]\n{doc.page_content}")
        return "\n\n---\n\n".join(parts)

    @staticmethod
    def delete_by_application(application_id: str) -> None:
        index = get_pinecone_index()
        try:
            index.delete(filter={"application_id": {"$eq": application_id}})
        except Exception:
            pass

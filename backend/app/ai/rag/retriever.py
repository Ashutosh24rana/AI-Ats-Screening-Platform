from functools import lru_cache


@lru_cache
def get_llm():
    """Configurable LLM provider with structured-output support."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    from app.core.config import settings

    return ChatGoogleGenerativeAI(
        model=settings.llm_model,
        google_api_key=settings.llm_api_key,
        temperature=0,
    )


class ResumeRetriever:
    """RAG retriever: builds a job-aware query, fetches top-k chunks from Pinecone."""

    def __init__(self):
        from app.ai.vectorstore.pinecone_client import ResumeVectorStore

        self.vector_store = ResumeVectorStore()

    def build_retrieval_query(self, job_title: str, job_description: str, required_skills: list[str]) -> str:
        skills_text = ", ".join(required_skills) if required_skills else "relevant skills"
        return (
            f"Candidate resume evidence for the role of {job_title}. "
            f"Looking for demonstrated experience with: {skills_text}. "
            f"Job requirements summary: {job_description[:600]}"
        )

    def retrieve(self, query: str, job_id: str, candidate_id: str):
        return self.vector_store.retrieve_for_candidate(query, job_id=job_id, candidate_id=candidate_id)

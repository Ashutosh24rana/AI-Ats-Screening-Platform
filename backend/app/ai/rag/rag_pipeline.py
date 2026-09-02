"""RAG pipeline: job-aware query -> Pinecone retrieval -> formatted context for the LLM."""

from app.ai.rag.retriever import ResumeRetriever
from app.ai.vectorstore.pinecone_client import ResumeVectorStore


class RAGPipeline:
    def __init__(self):
        self.retriever = ResumeRetriever()
        self.vector_store = ResumeVectorStore()

    def get_resume_context(
        self,
        job_title: str,
        job_description: str,
        required_skills: list[str],
        job_id: str,
        candidate_id: str,
    ) -> str:
        query = self.retriever.build_retrieval_query(job_title, job_description, required_skills)
        chunks = self.retriever.retrieve(query, job_id=job_id, candidate_id=candidate_id)
        return ResumeVectorStore.format_chunks(chunks) if chunks else ""

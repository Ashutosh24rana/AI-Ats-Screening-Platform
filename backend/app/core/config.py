from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str
    debug: bool
    api_v1_prefix: str
    base_dir: Path = BASE_DIR

    frontend_origin: str

    # Database
    database_url: str

    # Security
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    # Redis / Celery
    redis_url: str

    # Pinecone
    pinecone_api_key: str
    pinecone_index_name: str
    pinecone_cloud: str
    pinecone_region: str

    # AI
    llm_api_key: str
    llm_model: str
    embedding_model: str
    retrieval_top_k: int

    # Uploads
    upload_dir: str
    max_upload_size_mb: int

    # Shortlisting thresholds
    shortlist_threshold: int
    review_threshold: int

    model_config = {
        "env_file": str(BASE_DIR.parent / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "case_sensitive": False,
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "ai_ats",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.resume_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_time_limit=900,
    task_soft_time_limit=840,
    broker_connection_retry_on_startup=True,
)

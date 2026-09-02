"""Worker-side helpers for resume processing (used by Celery workers)."""

from app.tasks.resume_tasks import process_resume_task  # noqa: F401

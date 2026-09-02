import logging

from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.database.session import engine
from app.models import ProcessingStatus
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)

WorkerSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

MAX_RETRIES = 3
RETRY_COUNTDOWN_SECONDS = 30


@celery_app.task(
    bind=True,
    name="tasks.process_resume",
    max_retries=MAX_RETRIES,
    default_retry_delay=RETRY_COUNTDOWN_SECONDS,
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
)
def process_resume_task(self, application_id: str):
    """Celery entrypoint for the full resume-processing + AI-evaluation workflow.

    Task logic stays thin: it delegates to services (AI/RAG/LangGraph live there).
    """
    db = WorkerSession()
    try:
        from app.repositories.application_repository import ApplicationRepository

        repo = ApplicationRepository(db)
        repo.set_processing_status(application_id, ProcessingStatus.PROCESSING)

        from app.services.scoring_service import ScoringService

        ScoringService(db).evaluate_application(application_id)
        return {"application_id": application_id, "status": "COMPLETED"}
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        logger.exception("Resume processing failed for application %s", application_id)
        if self.request.retries < MAX_RETRIES:
            raise self.retry(exc=exc, countdown=RETRY_COUNTDOWN_SECONDS * (self.request.retries + 1))
        _mark_failed(db, application_id, str(exc))
        return {"application_id": application_id, "status": "FAILED", "error": str(exc)}
    finally:
        db.close()


def _mark_failed(db, application_id: str, error_message: str):
    """Keep the application but record the failure so the company can retry."""
    try:
        from app.repositories.application_repository import ApplicationRepository

        ApplicationRepository(db).set_processing_status(
            application_id, ProcessingStatus.FAILED, error_message[:2000]
        )
    except Exception:  # noqa: BLE001
        logger.exception("Could not mark application %s as failed", application_id)


@celery_app.task(name="tasks.retry_resume_processing")
def retry_resume_processing(application_id: str):
    return process_resume_task.delay(application_id).id


# Keep settings import referenced for env-driven config inside workers
_ = settings

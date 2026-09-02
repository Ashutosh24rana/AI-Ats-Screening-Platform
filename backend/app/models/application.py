import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.utils.id_generator import new_uuid


class ApplicationStatus:
    PENDING = "PENDING"
    SCREENING = "SCREENING"
    SHORTLISTED = "SHORTLISTED"
    REVIEW = "REVIEW"
    REJECTED = "REJECTED"

    ALL = [PENDING, SCREENING, SHORTLISTED, REVIEW, REJECTED]


class ProcessingStatus:
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    ALL = [PROCESSING, COMPLETED, FAILED]


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("job_id", "candidate_id", name="uq_application_job_candidate"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), index=True, nullable=False
    )
    resume_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), default=ApplicationStatus.PENDING, nullable=False)
    processing_status: Mapped[str] = mapped_column(String(20), default=ProcessingStatus.PROCESSING, nullable=False)
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    job: Mapped["Job"] = relationship(back_populates="applications")  # noqa: F821
    candidate: Mapped["Candidate"] = relationship(back_populates="applications")  # noqa: F821
    resume: Mapped["Resume | None"] = relationship()  # noqa: F821
    score: Mapped["CandidateScore | None"] = relationship(  # noqa: F821
        back_populates="application", uselist=False, cascade="all, delete-orphan"
    )

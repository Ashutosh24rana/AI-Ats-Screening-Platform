import uuid

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.utils.id_generator import new_uuid


class CandidateScore(Base):
    __tablename__ = "candidate_scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    application_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), unique=True, index=True, nullable=False
    )
    skill_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    experience_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ats_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    semantic_match_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    final_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    matched_skills: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    missing_skills: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    strengths: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    weaknesses: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommendation: Mapped[str | None] = mapped_column(String(100), nullable=True)

    application: Mapped["Application"] = relationship(back_populates="score")  # noqa: F821

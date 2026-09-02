"""initial schema - users, companies, jobs, candidates, resumes, applications, candidate_scores

Revision ID: 0001_initial
Revises:
Create Date: 2026-08-24
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "companies",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        ),
        sa.Column("company_name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("website", sa.String(255), nullable=True),
        sa.Column("logo_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "jobs",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "company_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("required_skills", pg.ARRAY(sa.Text()), nullable=False),
        sa.Column("preferred_skills", pg.ARRAY(sa.Text()), nullable=False),
        sa.Column("minimum_experience", sa.Integer(), nullable=False),
        sa.Column("location", sa.String(255), nullable=False),
        sa.Column("employment_type", sa.String(50), nullable=False),
        sa.Column("application_slug", sa.String(32), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f("ix_jobs_company_id"), "jobs", ["company_id"])
    op.create_index(op.f("ix_jobs_application_slug"), "jobs", ["application_slug"], unique=True)
    op.create_check_constraint(
        "ck_jobs_status", "jobs", "status IN ('DRAFT', 'PUBLISHED', 'CLOSED')"
    )
    op.create_check_constraint(
        "ck_jobs_employment_type",
        "jobs",
        "employment_type IN ('FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERNSHIP')",
    )

    op.create_table(
        "candidates",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f("ix_candidates_email"), "candidates", ["email"])

    op.create_table(
        "resumes",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "candidate_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("candidates.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("file_url", sa.String(500), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f("ix_resumes_candidate_id"), "resumes", ["candidate_id"])

    op.create_table(
        "applications",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "job_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("jobs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "candidate_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("candidates.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "resume_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("resumes.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("processing_status", sa.String(20), nullable=False),
        sa.Column("processing_error", sa.Text(), nullable=True),
        sa.Column("applied_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("job_id", "candidate_id", name="uq_application_job_candidate"),
    )
    op.create_index(op.f("ix_applications_job_id"), "applications", ["job_id"])
    op.create_index(op.f("ix_applications_candidate_id"), "applications", ["candidate_id"])
    op.create_check_constraint(
        "ck_applications_status",
        "applications",
        "status IN ('PENDING', 'SCREENING', 'SHORTLISTED', 'REVIEW', 'REJECTED')",
    )
    op.create_check_constraint(
        "ck_applications_processing_status",
        "applications",
        "processing_status IN ('PROCESSING', 'COMPLETED', 'FAILED')",
    )

    op.create_table(
        "candidate_scores",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "application_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("applications.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("skill_score", sa.Integer(), nullable=False),
        sa.Column("experience_score", sa.Integer(), nullable=False),
        sa.Column("ats_score", sa.Integer(), nullable=False),
        sa.Column("semantic_match_score", sa.Integer(), nullable=False),
        sa.Column("final_score", sa.Float(), nullable=False),
        sa.Column("matched_skills", pg.ARRAY(sa.Text()), nullable=False),
        sa.Column("missing_skills", pg.ARRAY(sa.Text()), nullable=False),
        sa.Column("strengths", pg.ARRAY(sa.Text()), nullable=False),
        sa.Column("weaknesses", pg.ARRAY(sa.Text()), nullable=False),
        sa.Column("ai_summary", sa.Text(), nullable=True),
        sa.Column("recommendation", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f("ix_candidate_scores_application_id"), "candidate_scores", ["application_id"], unique=True)


def downgrade() -> None:
    op.drop_table("candidate_scores")
    op.drop_table("applications")
    op.drop_table("resumes")
    op.drop_table("candidates")
    op.drop_table("jobs")
    op.drop_table("companies")
    op.drop_table("users")

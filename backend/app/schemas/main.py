from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr


# ---------- Auth ----------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    company_name: str
    description: str | None = None
    website: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | Any
    email: EmailStr


class MeResponse(BaseModel):
    user: UserResponse
    company: "CompanyResponse"


# ---------- Company ----------
class CompanyUpdate(BaseModel):
    company_name: str | None = None
    description: str | None = None
    website: str | None = None
    logo_url: str | None = None


class CompanyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | Any
    company_name: str
    description: str | None
    website: str | None
    logo_url: str | None


# ---------- Jobs ----------
class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    minimum_experience: int = 0
    location: str
    employment_type: str = "FULL_TIME"


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    minimum_experience: int | None = None
    location: str | None = None
    employment_type: str | None = None
    status: str | None = None


class JobStatusUpdate(BaseModel):
    status: str


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | Any
    title: str
    description: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: int
    location: str
    employment_type: str
    application_slug: str
    status: str
    created_at: datetime | None = None


class JobWithStats(JobResponse):
    applications_count: int = 0
    shortlisted_count: int = 0
    average_score: float | None = None


# ---------- Candidates / Applications ----------
class CandidateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | Any
    name: str
    email: str
    phone: str | None


class ScoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skill_score: int
    experience_score: int
    ats_score: int
    semantic_match_score: int
    final_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    ai_summary: str | None
    recommendation: str | None


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | Any
    job_id: str | Any
    candidate: CandidateResponse
    resume_id: str | Any | None
    status: str
    processing_status: str
    processing_error: str | None
    applied_at: datetime
    score: ScoreResponse | None


class CandidateStatusUpdate(BaseModel):
    status: str


# ---------- Public application ----------
class PublicJobResponse(BaseModel):
    title: str
    description: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: int
    location: str
    employment_type: str
    company_name: str


MeResponse.model_rebuild()

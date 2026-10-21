# AI ATS Platform

> **RAG + LangGraph Hiring Pipeline** — Publish jobs → share a public link → collect PDF resumes → AI scores every candidate with explainable skills, strengths, and a shortlist decision in ~40 seconds.

**No candidate accounts. One company login owns everything. Built as a production-style SaaS, not a demo.**

---

## 📋 Table of Contents

1. [Quick Demo](#-quick-demo)
2. [Features](#-features)
3. [Authentication Model](#-authentication-model)
4. [Tech Stack](#-tech-stack)
5. [Architecture](#-architecture)
6. [Folder Structure](#-folder-structure)
7. [Prerequisites](#-prerequisites)
8. [Environment Variables](#-environment-variables)
9. [Setup — 3 Terminals or 1 Click](#-setup--3-terminals-or-1-click)
10. [Database & Migrations](#-database--migrations)
11. [API Reference](#-api-reference)
12. [RAG Architecture](#-rag-architecture)
13. [LangGraph Workflow](#-langgraph-workflow)
14. [Chunking Strategy](#-chunking-strategy)
15. [Celery Processing Flow](#-celery-processing-flow)
15. [Scoring Methodology](#-scoring-methodology)
16. [Testing](#-testing)
16. [Troubleshooting](#-troubleshooting)
17. [Future Improvements](#-future-improvements)

---

## 🚀 Quick Demo

| Role | Flow |
|------|------|
| **Recruiter** | Register → Login → Dashboard → Create Job → Publish → Copy `/apply/{slug}` link |
| **Candidate** | Open `/apply/{slug}` → View job → Enter name/email/phone → Upload PDF → Submit → Success |
| **System** | Save → Queue Celery → Extract → Chunk → Embed → Pinecone → RAG → LangGraph → Shortlist |

**Live URLs (local):**

| Service | URL |
|---------|-----|
| Frontend | `http://localhost:5173` — Homepage `/`, Login `/login`, Dashboard `/dashboard`, Public apply `/apply/{slug}` |
| API | `http://localhost:8000` — Health `/health`, Swagger `/docs` |

---

## ✨ Features

| Category | Capability |
|----------|------------|
| **Auth** | Company-only JWT + bcrypt; one company profile per account; full ownership isolation |
| **Jobs** | CRUD with lifecycle `DRAFT → PUBLISHED → CLOSED`; unique slug; edit/publish/close/delete |
| **Public Apply** | `GET /public/jobs/{slug}` + `POST /public/jobs/{slug}/apply` (multipart); no auth; PDF + size validation; safe filenames; duplicate `(job_id, candidate_id)` blocked |
| **Async AI** | Celery + Redis; 3 retries with exponential backoff; `PROCESSING → COMPLETED/FAILED`; retry from dashboard |
| **RAG** | Job-aware query → Pinecone filtered retrieval (top-K=8) → section-tagged context for LLM |
| **LangGraph** | 10-node typed state graph with Pydantic-validated structured outputs |
| **Explainable Scores** | Matched/missing skills, strengths/weaknesses, ATS quality, natural-language summary, recommendation |
| **Dashboards** | Company stats; job ranking with filters (`All/Shortlisted/Review/Rejected`); candidate detail with score breakdown |

---

## 🔐 Authentication Model

```
Company User  (only row in `users` — email + password_hash)
     ↓ 1:1
Company Profile  (company_name, website — owns jobs)
     ↓ 1:N
Jobs  (application_slug unique, status DRAFT/PUBLISHED/CLOSED)
     ↓ 1:N
Applications  (job_id + candidate_id unique, status + processing_status)
     ↓ 1:1
CandidateScores  (skill, experience, semantic, ats, final, strengths, etc.)

Candidates  (name, email, phone) — never in `users`, no password/role/JWT
Resumes  (file_url, raw_text) — vectors live in Pinecone, not Postgres
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Vite, React Router, Tailwind CSS, Axios, Context API, React Hook Form, react-hot-toast |
| **Backend** | Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic, PyJWT, bcrypt |
| **Database** | PostgreSQL 18, `ARRAY(Text)`, `UUID`, constraints |
| **AI** | LangChain, LangGraph, Gemini `models/gemini-3.6-flash` + `models/gemini-embedding-001` (configurable) |
| **Vector DB** | Pinecone (metadata-filtered) |
| **Async** | Celery + Redis |

---

```


---

## 📁 Folder Structure

```text
Airesumeplatform/
├── .env                    # single env file for backend + frontend (VITE_*)
├── .vscode/tasks.json      # Run All (Ctrl+Shift+B) — Redis + API + Worker + Frontend
├── frontend/
│   ├── vite.config.js      # envDir: '../' → reads root .env
│   └── src/
│       ├── components/
│       │   ├── common/     # Spinner, StatusBadge, EmptyState, ConfirmDialog, ScoreIndicator
│       │   ├── layout/     # DashboardLayout (structural)
│       │   ├── home/       # HomeNavbar, Hero, PipelinePreview, HowItWorks, StepCard, Features
│       │   └── jobs/       # JobForm
│       ├── pages/
│       │   ├── Home.jsx            # composes home components
│       │   ├── auth/               # Login, Register
│       │   ├── dashboard/          # DashboardHome
│       │   ├── jobs/               # Jobs, CreateJob, EditJob, JobDetails
│       │   ├── candidates/         # Candidates, CandidateDetails
│       │   └── public/             # JobApplication, ApplicationSuccess
│       ├── hooks/          # useAuth, useInView
│       ├── services/       # api, authService, jobService, applicationService
│       ├── utils/          # constants, formatters, validators
│       └── routes/         # AppRoutes, ProtectedRoute
└── backend/
    ├── app/
    │   ├── core/           # config (reads root .env), security (JWT/bcrypt), dependencies
    │   ├── database/       # database.py (engine/Base/get_db) + session.py shim
    │   ├── models/         # user, company, job, candidate, resume, application, candidate_score
    │   ├── schemas/        # Pydantic request/response + AI evaluation schemas
    │   ├── api/routes/     # auth, jobs, applications, candidates, companies, public, stats
    │   ├── services/       # auth, company, job, application, candidate, scoring
    │   ├── repositories/   # user, company, job, application, candidate
    │   ├── ai/
    │   │   ├── loaders/        # resume_loader (PyPDF)
    │   │   ├── chunking/       # resume_chunker (section-aware)
    │   │   ├── embeddings/     # embedding_service (Gemini)
    │   │   ├── vectorstore/    # pinecone_client
    │   │   ├── rag/            # retriever, rag_pipeline, prompt_templates
    │   │   ├── langgraph/      # state, nodes, edges, workflow
    │   │   └── evaluation/     # skill_matcher, experience_evaluator, final_scorer
    │   ├── tasks/          # celery_app, resume_tasks (thin, 3 retries)
    │   ├── workers/        # resume_processing (re-export, placeholder)
    │   └── utils/          # file_utils, text_utils, id_generator
    ├── alembic/            # env.py, versions/0001_initial.py
    └── tests/              # test_auth, test_scoring, test_ai_pipeline
```

---

## ⚙️ Prerequisites

- **Python** 3.11+ (3.12 tested)
- **Node.js** 18+
- **PostgreSQL** 18 — running as Windows service `postgresql-x64-18` on `localhost:5432`
- **Redis** 5+ — `redis-server.exe` on `localhost:6379` (portable at `%LOCALAPPDATA%\Redis`)
- **Pinecone** account + API key
- **Gemini** API key (`LLM_API_KEY`)

---

## 🔐 Environment Variables

Single file: **`Airesumeplatform/.env`** (gitignored). Backend reads it via `backend/app/core/config.py:6` `BASE_DIR.parent / ".env"`, frontend via `frontend/vite.config.js:6` `envDir: '../'`.

| Variable | Example | Used in |
|----------|---------|---------|
| `DATABASE_URL` | `postgresql://postgres:123@localhost:5432/ResumeRAG` | `database.py:6` |
| `JWT_SECRET_KEY` / `JWT_ALGORITHM` / `ACCESS_TOKEN_EXPIRE_MINUTES` | `cantseeme` / `HS256` / `60` | `core/security.py` |
| `REDIS_URL` | `redis://localhost:6379/0` | `tasks/celery_app.py` |
| `PINECONE_API_KEY` / `PINECONE_INDEX_NAME` / `PINECONE_CLOUD` / `PINECONE_REGION` | `pcsk_...` / `resume-index` / `aws` / `us-east-1` | `ai/vectorstore/pinecone_client.py` |
| `LLM_API_KEY` / `LLM_MODEL` / `EMBEDDING_MODEL` / `RETRIEVAL_TOP_K` | `models/gemini-3.6-flash` / `models/gemini-embedding-001` / `8` | `ai/embeddings/*`, `ai/rag/*`, `ai/langgraph/*` |
| `UPLOAD_DIR` / `MAX_UPLOAD_SIZE_MB` | `uploads` / `10` | `services/application_service.py`, `utils/file_utils.py` |
| `SHORTLIST_THRESHOLD` / `REVIEW_THRESHOLD` | `75` / `60` | `ai/evaluation/final_scorer.py`, `services/scoring_service.py` |
| `FRONTEND_ORIGIN` | `http://localhost:5173` | `main.py` CORS |
| `VITE_API_BASE_URL` | `http://localhost:8000` | `frontend/src/services/api.js` |
| `APP_NAME` / `DEBUG` / `API_V1_PREFIX` | `AI ATS Platform` / `true` / `/api/v1` | `core/config.py`, `main.py` |


---

## 🚀 Setup — 3 Terminals or 1 Click

### One-click (VS Code)

`Ctrl+Shift+B` (or `Terminal → Run Task → Run All`) starts all 4 in parallel:

- Redis Server (`%LOCALAPPDATA%\Redis\redis-server.exe`)
- Backend API (`uvicorn app.main:app --reload --port 8000`)
- Celery Worker (`celery -A app.tasks.celery_app worker --pool=solo`)
- Frontend (`npm run dev` → `http://localhost:5173`)

> Auto-kills old processes before starting (no `WinError 10013`). Stop with `Terminal → Run Task → Stop All`.

### Manual

```powershell
# Terminal 1 — Redis
& "$env:LOCALAPPDATA\Redis\redis-server.exe"

# Terminal 2 — API (from backend/)
python -m uvicorn app.main:app --reload --port 8000

# Terminal 3 — Worker (from backend/)
python -m celery -A app.tasks.celery_app worker --pool=solo --loglevel=info

# Terminal 4 — Frontend (from frontend/)
npm run dev
```

### First-time Install

```powershell
# PostgreSQL — create DB once
$env:PGPASSWORD=''; & "D:\postgresql\bin\psql.exe" -h localhost -p 5432 -U postgres -c 'CREATE DATABASE "ResumeRAG";'

# Backend
cd backend
pip install -r requirements.txt
alembic upgrade head

# Frontend
cd ..\frontend
npm install
```

---

## 🗄 Database & Migrations

| File | Purpose |
|------|---------|
| `backend/app/database/database.py:1-20` | `engine`, `SessionLocal`, `Base`, `get_db` (dependency-injected) |
| `backend/app/database/session.py` | Compatibility shim re-exporting from `database.py` |

**Models** use `UUID`, `ARRAY(Text)`, `UniqueConstraint(job_id, candidate_id)`, check constraints for `status`.

| Command | Purpose |
|---------|---------|
| `alembic upgrade head` | Apply all migrations |
| `alembic revision --autogenerate -m "msg"` | Generate new migration |
| `alembic downgrade -1` | Rollback one migration |

**Initial migration** `alembic/versions/0001_initial.py` creates 7 tables: `users`, `companies`, `jobs`, `candidates`, `resumes`, `applications`, `candidate_scores` + `alembic_version`.

---

## 📡 API Reference

Swagger: `http://localhost:8000/docs`

### Auth — Company Only (`/api/v1/auth`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | ❌ | `{email, password, company_name, website?, description?}` → `User + Company` → JWT |
| `POST` | `/auth/login` | ❌ | `{email, password}` → JWT |
| `GET` | `/auth/me` | ✅ | Current user + company |

### Jobs (`/api/v1/jobs`) — Protected, Ownership-checked

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/jobs` | List own jobs with `applications_count`, `shortlisted_count`, `average_score` |
| `POST` | `/jobs` | Create (auto `application_slug`, `DRAFT`) |
| `GET` | `/jobs/{id}` | Single job |
| `PATCH` | `/jobs/{id}` | Update title/description/skills/location/status |
| `POST` | `/jobs/{id}/status` | `{"status":"PUBLISHED\|CLOSED\|DRAFT"}` |
| `DELETE` | `/jobs/{id}` | Delete (cascades applications) |
| `GET` | `/jobs/{id}/applications` | Ranked candidates + `counts{total,shortlisted,review,rejected}` |

### Applications / Candidates — Protected

| Method | Endpoint |
|--------|----------|
| `GET` | `/applications` / `/applications/{id}` |
| `POST` | `/applications/{id}/status` `{"status":"SHORTLISTED\|REVIEW\|REJECTED\|..."}` |
| `POST` | `/applications/{id}/retry` (re-queue `FAILED` → `PROCESSING`) |
| `GET` | `/applications/{id}/resume` (PDF download) |
| `GET` | `/candidates/dashboard-stats` `{total_jobs, active_jobs, total_applications, shortlisted}` |

### Public — No Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/public/jobs/{slug}` | Job + company for apply page (404 if `DRAFT`/`CLOSED`) |
| `POST` | `/public/jobs/{slug}/apply` | `multipart/form-data` `name, email, phone?, resume(PDF)` → `201` + Celery task |

---

## 🔍 RAG Architecture

Full resume is **never** sent to the LLM:

```
Job title + required_skills + description
  → build_retrieval_query()  (retriever.py)
  → Pinecone similarity search  (index: resume-index, filter: {job_id, candidate_id}, k=8)
  → [experience]/[skills] tagged excerpts
  → structured LLM nodes
```

**Vectors:** `PineconeVectorStore` + `GoogleGenerativeAIEmbeddings(models/gemini-embedding-001)`, metadata `{candidate_id, application_id, job_id, resume_id, section, chunk_index}`. Retrieval is always scoped to the current application.

---

## 🧠 LangGraph Workflow

`backend/app/ai/langgraph/workflow.py:12`

```
START → parse_resume_information (PyPDF → clean → section-aware chunk → embed → Pinecone)
      → retrieve_relevant_chunks (job-aware RAG, k=8)
      → evaluate_skill_match (LLM SkillEvaluation + regex SkillMatcher 60/40)
      → evaluate_experience (LLM + regex year patterns)
      → evaluate_semantic_match
      → evaluate_ats_quality
      → calculate_final_score (pure math)
      → generate_candidate_summary (FinalEvaluation)
      → make_shortlisting_decision (thresholds)
      → save_results → END
      ↘ handle_error → END
```

- **State:** `ai/langgraph/state.py` (`EvaluationState` TypedDict)
- Each node uses `with_structured_output(Pydantic)` — malformed LLM JSON is retried by LangChain
- Thresholds from `SHORTLIST_THRESHOLD` / `REVIEW_THRESHOLD`

---

## 📦 Chunking Strategy

`backend/app/ai/chunking/resume_chunker.py` — **Detect → Split → Tag**:

1. **Detect** headings via regex `^\s*(work experience|education|skills|...)\s*:?\s*$` (multiline, case-insensitive, longest hint wins), sorted by position
2. **Split** `text[heading_end : next_heading_start]` per section with `RecursiveCharacterTextSplitter(800, 120, ["\n\n", "\n", ". ", " ", ""])` — paragraphs stay together, 120 overlap prevents boundary loss
3. **Tag** every `Document` with `{section, chunk_index}` + base metadata; fallback to blind split as `other` if no headings found

> Previous blind 800-char splitter is kept as fallback for creative layouts.

---

## ⚙️ Celery Processing Flow

1. FastAPI validates, saves `candidate + resume + application(PROCESSING)`, `process_resume_task.delay(id)` → Redis
2. Worker `resume_tasks.py:29` → `ScoringService.evaluate_application` → LangGraph
3. Success → `candidate_scores` row, `COMPLETED`, status `SHORTLISTED≥75 / REVIEW≥60 / REJECTED`
4. Failure → 3 retries (30s, 60s, 90s backoff) → `FAILED` + `processing_error` kept, retryable via `POST /applications/{id}/retry`

> Redis is **only** the broker — no direct `redis.get/set` in app code; Celery handles `RPUSH/BRPOP` internally.

---

## 📊 Scoring Methodology

| Component | Weight | Source |
|-----------|--------|--------|
| Skill Match | 40% | LLM + deterministic `SkillMatcher` regex |
| Experience | 25% | LLM + `ExperienceEvaluator` (year patterns + date ranges) |
| Semantic Fit | 20% | LLM holistic fit |
| ATS Quality | 15% | LLM structure/quantification check |

`final = skill*0.40 + exp*0.25 + sem*0.20 + ats*0.15` (`ai/evaluation/final_scorer.py`). All 0–100, Pydantic-validated.

---

## 🧪 Testing

```powershell
cd backend
python -m pytest tests -q          # 9 unit tests (auth, scoring, skill_matcher)
python -m compileall -q app        # import check
cd ..\frontend
npm run build                      # Vite build check
```

---

## 🛠 Troubleshooting

| Symptom | Fix |
|---------|-----|
| `WinError 10013` on `uvicorn` | Port 8000 busy — `Terminal → Run Task → Stop All` then `Ctrl+Shift+B`, or kill `Get-CimInstance Win32_Process \| ? CommandLine -like '*uvicorn*'` |
| `Get-CimInstance : Invalid query` | Fixed — tasks use `Where-Object { $_.Name -eq 'python.exe' }` not `-Filter` |
| White flash on homepage scroll | Fixed — `Home.jsx` outer `bg-slate-950` + `body #020617`, `useInView` re-triggers every scroll |
| Job counts show 0 / `applications_count` missing | Fixed — `jobs.py` now returns `JobWithStats` (was stripping counts) |
| Resume stuck `SCREENING` | Check `celery.err.log` + `processing_error` in DB; common causes: `gemini-embedding-2` → `models/gemini-embedding-001`, `gemini-2.0-flash` → `models/gemini-3.6-flash` |
| Login fails after Register | Fixed — `auth_service.py` / `job_service.py` now `commit()` after `flush()` |

---

## 🚀 Future Improvements

- Bulk upload + CSV export
- Side-by-side candidate comparison
- Streaming progress via WebSockets
- Email notifications
- Multi-recruiter roles
- Docker Compose one-command setup

---

from fastapi import APIRouter

from app.api.routes import applications, auth, candidates, companies, jobs, public, stats

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(companies.router)
api_router.include_router(jobs.router)
api_router.include_router(candidates.router)
api_router.include_router(applications.router)
api_router.include_router(public.router)
api_router.include_router(stats.router)

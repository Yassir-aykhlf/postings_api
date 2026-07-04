from datetime import datetime, timezone
from fastapi import APIRouter, Query
from app.schemas.job import JobCreate, JobRead

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("", summary="List jobs")
async def list_jobs(
    limit: int = Query(default=20, ge=0, le=1000),
    offset: int = Query(default=0, ge=0)
    ) ->dict:
    return {"items": [], "limit": limit, "offset": offset}

@router.get("/{job_id}", summary="Fetch a single job")
async def get_job(job_id: int) -> dict:
    return {"job_id": job_id}

@router.post("", response_model=JobRead, status_code=201)
async def create_job(payload: JobCreate) -> dict:
    now = datetime.now(timezone.utc)
    return {
        **payload.model_dump(),
        "id": 1,
        "status": "draft",
        "created_at": now,
        "updated_at": now,
        # must be stripped
        "owner_id": 999,
        "internal_secret": "do not leak",
        "is_deleted": False
    }
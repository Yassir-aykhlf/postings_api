from datetime import datetime, timezone
from fastapi import APIRouter, Query
from app.schemas.job import JobCreate, JobRead
from app.errors import NotFoundError

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("")
async def list_jobs(
    limit: int = Query(default=20, ge=0, le=100),
    offset: int = Query(default=0, ge=0)
) ->dict:
    return {"limit": limit, "offset": offset, "items": []}

@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: int) -> dict:
    raise NotFoundError(f"job {job_id} not found")

@router.post("", response_model=JobRead, status_code=201)
async def create_job(payload: JobCreate) -> dict:
    now = datetime.now(timezone.utc)
    return {
        **payload.model_dump(),
        "id": 1,
        "status": "draft",
        "created_at": now,
        "updated_at": now,
    }
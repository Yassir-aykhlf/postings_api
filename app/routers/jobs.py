from fastapi import APIRouter

router = APIRouter(prefix="jobs", tags=["jobs"])

@router.get("", summary="List jobs")
async def list_jobs(limit: int = 20):
    pass

@router.get("/{job_id}", summary="Fetch a single job")
async def get_job(job_id: int):
    pass
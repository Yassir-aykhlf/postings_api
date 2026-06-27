from fastapi import APIRouter
from fastapi import JSONResponse
from app.core.db import ping_db

router = APIRouter(tags=["health"])

@router.get("/health")
async def health() -> JSONResponse:
    try:
        await ping_db()
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "degraded", "database": "unreachable"}
        )
    return JSONResponse(
        status_code=200,
        content={"status": "ok", "database": "reachable"}
    )
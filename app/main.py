from fastapi import FastAPI
from app.routers import health, jobs
from app.errors import install_error_handlers

app = FastAPI(
    title="Postings",
    version="0.1.0"
)
install_error_handlers(app)
app.include_router(health.router)
app.include_router(jobs.router)
from fastapi import FastAPI
from app.routers import health, jobs

def create_app():
    app = FastAPI(
        title="Postings",
        version="0.1.0"
    )
    app.include_router(health.router)
    app.include_router(jobs.router)
    return app

app = create_app()
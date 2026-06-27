from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postings"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine)

async def ping_db() -> bool:
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))
    return True
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import get_settings

DATABASE_URL = get_settings().database_url

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine)

async def ping_db() -> bool:
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))
    return True
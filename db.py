from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from core.config import settings

engine = create_async_engine(
    settings.database_url
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

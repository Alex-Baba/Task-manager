from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from collections.abc import AsyncGenerator
from app.core import get_config

# get database url
config = get_config()

# shared async engine used for all database connect
engine = create_async_engine(config.database_url)

# factory that creates 1 async SQLAlchemy session
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# async generator for session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session



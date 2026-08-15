import os
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db.models import Base
from dotenv import load_dotenv
load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL, 
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
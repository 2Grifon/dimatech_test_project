from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core.config import settings

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,
)

AsyncSessionFactory = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

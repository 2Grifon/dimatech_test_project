from typing import Annotated, AsyncGenerator

from fastapi import Depends
from redis.asyncio import Redis, ConnectionPool

from app.core.config import settings

redis_pool = ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)


async def get_redis() -> AsyncGenerator[Redis, None]:
    client = Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await client.aclose()


RedisDep = Annotated[Redis, Depends(get_redis)]

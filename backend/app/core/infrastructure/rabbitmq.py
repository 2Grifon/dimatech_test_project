from typing import AsyncGenerator
import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractChannel

from app.core.config import settings

_connection: AbstractRobustConnection | None = None


async def get_rabbitmq_connection() -> AbstractRobustConnection:
    global _connection
    if _connection is None or _connection.is_closed:
        _connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    return _connection


async def get_channel() -> AsyncGenerator[AbstractChannel, None]:
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    try:
        yield channel
    finally:
        await channel.close()

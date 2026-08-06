from datetime import datetime, timezone

from app.core.redis import RedisDep

BLACKLIST_KEY_PREFIX = "blacklist:jti:"


async def blacklist_token(redis: RedisDep, jti: str, exp: float) -> None:
    """Добавляет jti в blacklist с TTL до истечения токена (exp — unix timestamp)."""
    now: float = datetime.now(timezone.utc).timestamp()
    ttl = int(exp - now)

    if ttl <= 0:
        return  # токен уже истёк, блэклистить незачем

    await redis.set(f"{BLACKLIST_KEY_PREFIX}{jti}", "1", ex=ttl)


async def is_token_blacklisted(redis: RedisDep, jti: str) -> bool:
    return await redis.exists(f"{BLACKLIST_KEY_PREFIX}{jti}") == 1

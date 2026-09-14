import jwt
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from app.core.config import settings


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    expire = (datetime.now(timezone.utc) + expires_delta).timestamp()
    to_encode: dict = {
        "exp": expire,
        "sub": str(subject),
        "jti": str(uuid.uuid4()),
    }

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.HASHING_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.HASHING_ALGORITHM],
    )

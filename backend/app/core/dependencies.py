# app/core/dependencies.py
import uuid
from typing import Annotated

from jwt import InvalidTokenError
from pydantic import ValidationError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from app.core.config import settings
from app.core.db import SessionDep
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.core.redis import RedisDep
from app.core.security import decode_access_token
from app.core.token_blacklist import is_token_blacklisted
from app.modules.users.models import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
    redis: RedisDep,
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        jti = payload.get("jti")
        if user_id is None or jti is None:
            raise UnauthorizedException(
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (InvalidTokenError, ValidationError):
        raise UnauthorizedException(
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if await is_token_blacklisted(redis, jti):
        raise UnauthorizedException(
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await session.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()

    if user is None:
        raise UnauthorizedException(
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role != UserRole.admin:
        raise ForbiddenException(detail="Admin privileges required")
    return current_user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
CurrentAdminDep = Annotated[User, Depends(get_current_admin)]

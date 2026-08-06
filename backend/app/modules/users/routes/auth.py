# app/modules/users/routes/auth.py
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.core.db import SessionDep
from app.core.dependencies import oauth2_scheme
from app.core.exceptions import UnauthorizedException
from app.core.redis import RedisDep
from app.core.security import create_access_token, decode_access_token, verify_password
from app.core.token_blacklist import blacklist_token
from app.modules.users.models import User
from app.modules.users.schemas import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    # TODO: Вытащить логику в класс-зависимость? В отдельную функцию?
    if user is None:
        raise UnauthorizedException(detail="Invalid email or password")

    verified, updated_hash = verify_password(form_data.password, user.hashed_password)

    if not verified:
        raise UnauthorizedException(detail="Invalid email or password")

    if updated_hash is not None:
        user.hashed_password = updated_hash
        session.add(user)
        await session.commit()

    return Token(access_token=create_access_token(user.id), token_type="bearer")


@router.post("/logout")
async def logout(
    token: Annotated[str, Depends(oauth2_scheme)],
    redis: RedisDep,
) -> dict[str, str]:
    payload = decode_access_token(token)
    await blacklist_token(redis, jti=payload["jti"], exp=payload["exp"])
    return {"detail": "Successfully logged out"}

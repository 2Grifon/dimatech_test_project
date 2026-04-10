from typing import Annotated, Sequence
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, delete

from app.core.db import SessionDep
from app.core.exceptions import NotFoundException, ConflictException
from app.core.security import get_password_hash
from app.modules.accounting.models.account import Account
from app.modules.users.models.user import User
from app.modules.users.schemas.user import UserCreate, UserUpdate


class AdminService:
    def __init__(self, session: SessionDep) -> None:
        self.session = session

    async def _get_user_or_404(self, user_id: UUID) -> User:
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")
        return user

    async def _assert_email_free(self, email: str, exclude_id: UUID | None = None) -> None:
        query = select(User).where(User.email == email)
        if exclude_id:
            query = query.where(User.id != exclude_id)
        existing = (await self.session.execute(query)).scalar_one_or_none()
        if existing:
            raise ConflictException(f"User with email '{email}' already exists")

    async def get_users(self) -> Sequence[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def create_user(self, data: UserCreate) -> User:
        await self._assert_email_free(data.email)

        user = User(
            email=data.email,
            full_name=data.full_name,
            role=data.role,
            hashed_password=get_password_hash(data.password),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user_id: UUID, data: UserUpdate) -> User:
        user = await self._get_user_or_404(user_id)

        update_data = data.model_dump(exclude_unset=True)

        if "email" in update_data:
            await self._assert_email_free(update_data["email"], exclude_id=user_id)

        if "password" in update_data:
            user.hashed_password = get_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: UUID) -> None:
        await self._get_user_or_404(user_id)
        await self.session.execute(delete(User).where(User.id == user_id))
        await self.session.commit()

    async def get_user_accounts(self, user_id: UUID) -> Sequence[Account]:
        await self._get_user_or_404(user_id)
        result = await self.session.execute(select(Account).where(Account.user_id == user_id))
        return result.scalars().all()


AdminServiceDep = Annotated[AdminService, Depends(AdminService)]

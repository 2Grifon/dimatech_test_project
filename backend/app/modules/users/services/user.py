from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from app.core.db import SessionDep

from app.modules.accounting.models import Account, Payment
from app.modules.users.models.user import User


class UserService:
    def __init__(self, session: SessionDep) -> None:
        self.session = session

    async def get_accounts(self, user: User):
        result = await self.session.execute(select(Account).where(Account.user_id == user.id))
        return result.scalars().all()

    async def get_payments(self, user: User):
        result = await self.session.execute(select(Payment).where(Payment.user_id == user.id))
        return result.scalars().all()


UserServiceDep = Annotated[UserService, Depends(UserService)]

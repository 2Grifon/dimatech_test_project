from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from app.core.db import SessionDep

from app.core.dependencies import CurrentUserDep
from app.modules.accounting.models import Account, Payment


class UserService:
    def __init__(self, session: SessionDep, current_user: CurrentUserDep) -> None:
        self.session = session
        self.current_user = current_user

    async def get_accounts(self):
        result = await self.session.execute(
            select(Account).where(Account.user_id == self.current_user.id)
        )
        return result.scalars().all()

    async def get_payments(self):
        result = await self.session.execute(
            select(Payment).where(Payment.user_id == self.current_user.id)
        )
        return result.scalars().all()


UserServiceDep = Annotated[UserService, Depends(UserService)]

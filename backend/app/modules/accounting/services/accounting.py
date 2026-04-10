from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.db import SessionDep
from app.core.exceptions import ConflictException

from app.modules.accounting.models import Account, Payment
from app.modules.accounting.schemas import WebhookPayload


class AccountingService:
    def __init__(self, session: SessionDep) -> None:
        self.session = session

    async def process_webhook(self, payload: WebhookPayload) -> Payment:
        print("transaction_id", payload.transaction_id)
        # Проверка на повторную обработку транзакции
        existing = await self.session.execute(
            select(Payment).where(Payment.transaction_id == payload.transaction_id)
        )
        if existing.scalar_one_or_none():
            raise ConflictException(f"Transaction '{payload.transaction_id}' already processed")

        # Получение счёта
        result = await self.session.execute(
            select(Account).where(
                Account.id == payload.account_id,
                Account.user_id == payload.user_id,
            )
        )
        account = result.scalar_one_or_none()

        # Создание счёта, если его нет
        if account is None:
            account = Account(
                id=payload.account_id,
                user_id=payload.user_id,
                balance=payload.amount,
            )
            self.session.add(account)
        else:
            account.balance += payload.amount  # Обновление баланса

        # Сохранение транзакции
        payment = Payment(
            transaction_id=payload.transaction_id,
            user_id=payload.user_id,
            account_id=payload.account_id,
            amount=payload.amount,
        )
        self.session.add(payment)

        # Атомарный коммит пополнения счёта и сохранения транзакции
        try:
            await self.session.commit()
        except IntegrityError:  # Транзакция раздвоилась
            await self.session.rollback()
            raise ConflictException(f"Transaction '{payload.transaction_id}' already processed")

        await self.session.refresh(payment)
        return payment


AccountingServiceDep = Annotated[AccountingService, Depends(AccountingService)]

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class PaymentRead(BaseModel):
    id: UUID
    transaction_id: str

    user_id: UUID
    account_id: UUID

    amount: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}

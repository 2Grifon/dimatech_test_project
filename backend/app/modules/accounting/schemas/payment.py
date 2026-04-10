from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class PaymentRead(BaseModel):
    id: UUID
    transaction_id: UUID

    user_id: UUID
    account_id: UUID

    amount: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class AccountRead(BaseModel):
    id: UUID
    user_id: UUID
    balance: Decimal

    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

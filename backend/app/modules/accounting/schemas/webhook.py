import hashlib
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, model_validator

from app.core.config import settings


class WebhookPayload(BaseModel):
    transaction_id: UUID
    user_id: UUID
    account_id: UUID
    amount: Decimal
    signature: str

    @model_validator(mode="before")
    @classmethod
    def verify_signature(cls, data: dict) -> dict:
        signature = data.get("signature")
        if not signature:
            raise ValueError("Missing signature")

        # {account_id}{amount}{transaction_id}{user_id}{secret_key}
        ordered_keys = sorted(k for k in data if k != "signature")
        payload_string = "".join(str(data[k]) for k in ordered_keys)
        payload_string += settings.PAYMENT_SECRET_KEY

        expected = hashlib.sha256(payload_string.encode()).hexdigest()

        if signature != expected:
            raise ValueError("Invalid signature")

        return data

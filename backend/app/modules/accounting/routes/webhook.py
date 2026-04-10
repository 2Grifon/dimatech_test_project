from fastapi import APIRouter, status

from app.modules.accounting.schemas import PaymentRead
from app.modules.accounting.schemas import WebhookPayload
from app.modules.accounting.services import AccountingServiceDep

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("/payment", status_code=status.HTTP_200_OK)
async def payment_webhook(
    payload: WebhookPayload,
    service: AccountingServiceDep,
) -> PaymentRead:
    payment = await service.process_webhook(payload)
    return payment

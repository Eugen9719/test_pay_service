
from fastapi import APIRouter
from backend.app.dependencies.services import payment_service
from backend.app.models.schemas import WebhookRequest
from backend.core.db import TransactionSessionDep

webhook_router = APIRouter()


@webhook_router.post("/process-payment-webhook")
async def process_payment_webhook(
        webhook_data: WebhookRequest,
        db: TransactionSessionDep
):
    return await payment_service.process_payment(db, webhook_data)

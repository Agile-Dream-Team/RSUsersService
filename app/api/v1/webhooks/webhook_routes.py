# app/api/v1/webhooks/webhook_routes.py
from fastapi import APIRouter
from app.dto.webhook_in_dto import WebhookDTO
from app.services.webhook_receiver_service import WebhookReceiverService
from app.responses.custom_responses import SuccessResponse, ErrorResponse

router = APIRouter()


@router.post("/webhooks")
async def receive_webhook(webhook: WebhookDTO):
    print(webhook)
    if not webhook:
        return ErrorResponse(detail="Webhook data is empty")

    webhook_receiver_service = WebhookReceiverService()

    received_data = webhook_receiver_service.receive_webhook(webhook)
    print(received_data.dict())
    return SuccessResponse(data=received_data.dict())

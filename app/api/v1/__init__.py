from fastapi import APIRouter
from .webhooks.webhook_routes import router as webhook_router

api_router = APIRouter()
api_router.include_router(webhook_router, prefix="/webhooks", tags=["webhooks"])
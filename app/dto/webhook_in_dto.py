# app/dto/webhook_in_dto.py
from typing import Optional
from pydantic import BaseModel, model_validator, ValidationInfo
from app.api.v1.utils import EventType


class WebhookDataDTO(BaseModel):
    temperature: Optional[str] = None
    humidity: Optional[str] = None
    electrical_conductivity: Optional[str] = None
    co2: Optional[str] = None
    camera_data: Optional[str] = None


class WebhookDTO(BaseModel):
    event: EventType
    data: WebhookDataDTO
    date_time: str
    client_id: str
    uuid: str

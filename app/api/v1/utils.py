from fastapi import Request
from app.exceptions.custom_exceptions import BadRequestException
from enum import Enum


async def validate_webhook(request: Request):
    if not request.json():
        raise BadRequestException(detail="Not a valid request")
    return await request.json()


class EventType(str, Enum):
    NORMAL = "normal"
    HIGH_TEMP = "high_temp"
    LOW_TEMP = "low_temp"
    HIGH_HUMIDITY = "high_humidity"
    LOW_HUMIDITY = "low_humidity"
    HIGH_CO2 = "high_co2"
    LOW_CO2 = "low_co2"
    HIGH_ELECTRICITY = "high_electricity"
    LOW_ELECTRICITY = "low_electricity"
    CAM_ALERT = "cam_alert"
    UNKNOWN = "unknown"

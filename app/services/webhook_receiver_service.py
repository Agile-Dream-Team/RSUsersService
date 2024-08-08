from app.dto.webhook_in_dto import WebhookDTO
from app.api.v1.utils import EventType
from app.exceptions.custom_exceptions import BadRequestException


def check_event_type(event: EventType):
    print(f"Checking event type: {event}")

    match event:
        case EventType.NORMAL:
            print("Event type is NORMAL")
        case EventType.HIGH_TEMP:
            print("Event type is HIGH_TEMP")
        case EventType.LOW_TEMP:
            print("Event type is LOW_TEMP")
        case EventType.HIGH_HUMIDITY:
            print("Event type is HIGH_HUMIDITY")
        case EventType.LOW_HUMIDITY:
            print("Event type is LOW_HUMIDITY")
        case EventType.HIGH_CO2:
            print("Event type is HIGH_CO2")
        case EventType.LOW_CO2:
            print("Event type is LOW_CO2")
        case EventType.HIGH_ELECTRICITY:
            print("Event type is HIGH_ELECTRICITY")
        case EventType.LOW_ELECTRICITY:
            print("Event type is LOW_ELECTRICITY")
        case EventType.CAM_ALERT:
            print("Event type is CAM_ALERT")
        case EventType.UNKNOWN:
            print("Event type is UNKNOWN")
        case _:
            raise BadRequestException(detail=f"Invalid event type: {event}")


class WebhookReceiverService:

    def __init__(self):
        pass

    def receive_webhook(self, webhook_data: WebhookDTO):
        check_event_type(webhook_data.event)
        return webhook_data

from pydantic import BaseModel
from typing import Optional
from app.utils.utils import EventType


class KafkaInDataDTO(BaseModel):
    temperature: Optional[str] = None
    humidity: Optional[str] = None
    electrical_conductivity: Optional[str] = None
    co2: Optional[str] = None
    camera_data: Optional[str] = None


class KafkaInDTO(BaseModel):
    event: EventType
    data: KafkaInDataDTO
    date_time: str
    client_id: str
    uuid: str

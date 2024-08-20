from pydantic import BaseModel
from typing import Optional
from app.utils.utils import EventType, EventActionConsume


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


class KafkaGetAllDTO(BaseModel):
    event: EventActionConsume


class KafkaGetByIdDTO(BaseModel):
    event: EventActionConsume
    client_id: str

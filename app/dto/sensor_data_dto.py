from pydantic import BaseModel
from typing import Optional
from app.utils.utils import TopicActionRequest


class KafkaInDataDTO(BaseModel):
    temperature_global: Optional[str] = None
    temperature_local: Optional[str] = None
    humidity_global: Optional[str] = None
    humidity_local: Optional[str] = None
    movement: Optional[bool] = None
    electrical_conductivity: Optional[str] = None
    air_flow: Optional[str] = None
    weight: Optional[str] = None
    light_intensity: Optional[str] = None


class KafkaInDTO(BaseModel):
    event_id: str
    data: KafkaInDataDTO
    date_time: str
    bucket_id: str
    uuid: str


class KafkaGetAllDTO(BaseModel):
    event: TopicActionRequest


class KafkaGetByIdDTO(BaseModel):
    event_id: str
    bucket_id: str

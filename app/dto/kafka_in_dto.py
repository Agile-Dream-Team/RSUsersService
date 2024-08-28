from pydantic import BaseModel
from typing import Optional, Union
from app.utils.utils import TopicEvent, TopicActionRequest


class KafkaInDataDTO(BaseModel):
    temperature_global: Optional[str] = None
    temperature_local: Optional[str] = None
    humidity_global: Optional[str] = None
    humidity_local: Optional[str] = None
    movement: Optional[bool] = None
    electrical_conductivity: Optional[str] = None
    air_flow: Optional[str] = None
    weight: Optional[str] = None


class KafkaInDTO(BaseModel):
    event: Union[TopicEvent, TopicActionRequest]
    data: KafkaInDataDTO
    date_time: str
    client_id: str
    uuid: str


class KafkaGetAllDTO(BaseModel):
    event: TopicActionRequest


class KafkaGetByIdDTO(BaseModel):
    event: TopicActionRequest
    client_id: str

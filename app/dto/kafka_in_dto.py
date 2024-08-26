from pydantic import BaseModel
from typing import Optional, Union
from app.utils.utils import TopicEvent, TopicActionRequest


class KafkaInDataDTO(BaseModel):
    temperature: Optional[str] = None
    humidity: Optional[str] = None
    electrical_conductivity: Optional[str] = None
    co2: Optional[str] = None
    camera_data: Optional[str] = None


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

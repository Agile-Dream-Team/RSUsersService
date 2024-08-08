from pydantic import BaseModel
from typing import Dict


class KafkaInDTO(BaseModel):
    event: str
    data: Dict

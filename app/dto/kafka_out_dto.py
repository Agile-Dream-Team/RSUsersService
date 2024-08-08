from pydantic import BaseModel
from typing import Dict


class KafkaOutDTO(BaseModel):
    data: Dict
    source: str

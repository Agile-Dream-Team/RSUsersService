from pydantic import BaseModel
from typing import Dict

class KafkaOutDTO(BaseModel):
    event: str
    data: Dict
    source: str
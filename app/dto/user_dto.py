from pydantic import BaseModel
from typing import Optional


class KafkaInDTO(BaseModel):
    cognito_sub: str
    email: str
    name: str
    family_name: str
    created_at: str

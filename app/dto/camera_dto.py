from pydantic import BaseModel


class KafkaInDTO(BaseModel):
    image_b64: str
    sensor_data_id: str

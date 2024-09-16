import json
from app.dto.camera_dto import KafkaInDTO
from app.domain.camera import Camera


def dto_to_entity(kafka_in_dto: str) -> Camera:
    try:
        # Parse the JSON string to KafkaInDTO
        kafka_in_dto = KafkaInDTO(**json.loads(kafka_in_dto))

        return Camera(
            image_b64=kafka_in_dto.image_b64,
            sensor_data_id=int(kafka_in_dto.sensor_data_id)
        )
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")

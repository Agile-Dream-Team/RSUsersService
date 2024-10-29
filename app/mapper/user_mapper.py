import json
from datetime import datetime
from app.domain.user import User
from app.dto.user_dto import KafkaInDTO


def dto_to_entity(kafka_in_dto) -> User:
    try:
        # Parse the JSON string to KafkaInDTO
        kafka_in_dto = KafkaInDTO(**kafka_in_dto)

        # Convert datetime string to datetime object
        datetime_obj = datetime.strptime(kafka_in_dto.created_at, '%Y-%m-%d %H:%M:%S')

        return User(
            cognito_sub=kafka_in_dto.cognito_sub,
            email=kafka_in_dto.email,
            name=kafka_in_dto.name,
            family_name=kafka_in_dto.family_name,
            created_at=datetime_obj
        )
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")


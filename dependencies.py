import os

from app.config.kafka_manager import KafkaManager
from app.services.kafka_producer_service import KafkaProducerService

# dependencies.py
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


async def has_access(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Function that is used to validate the token in the case that it requires it
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, key='secret', algorithms=["HS256"], options={"verify_signature": False,
                                                                                 "verify_aud": False,
                                                                                 "verify_iss": False})
        print("payload => ", payload)
    except InvalidTokenError as e:  # catches any exception
        raise HTTPException(
            status_code=401,
            detail=str(e))


def get_kafka_producer_service() -> KafkaProducerService:
    return KafkaProducerService(KafkaManager(
        bootstrap_servers=f'{os.getenv("KAFKA_HOST")}:{os.getenv("KAFKA_PORT")}',
        topics=os.getenv('KAFKA_TOPIC'),
        group_id=os.getenv('KAFKA_GROUP_ID')
    ))


def startup_kafka_manager(app, settings):
    app.state.kafka_manager = KafkaManager(
        bootstrap_servers=f'{settings.kafka_host}:{settings.kafka_port}',
        topics=settings.kafka_topics,  # Ensure topics are split into a list
        group_id=settings.kafka_group_id
    )
    app.state.kafka_producer_service = KafkaProducerService(app.state.kafka_manager)

import json
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel, ValidationError

from app.config.config import Settings
from app.config.database import setup_database
from RSKafkaWrapper.client import KafkaClient
from app.services.user_service import UserService


def configure_logging():
    logging.basicConfig(level=logging.INFO)


configure_logging()

app_settings = Settings()
app = FastAPI()

# Initialize KafkaClient using the singleton pattern
kafka_client = KafkaClient.instance(app_settings.kafka_bootstrap_servers, app_settings.kafka_group_id)

# Initialize the database and session
db_session = setup_database(app_settings)


# Dependency to get the KafkaConsumerService instance
def get_kafka_service_user():
    return UserService(kafka_client, db_session)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    try:
        local_settings = Settings()
    except ValidationError as e:
        logging.error(f"Environment variable validation error: {e}")
        raise

    existing_topics = kafka_client.list_topics()
    logging.info(f"Creating Kafka topics: {local_settings.kafka_topics}")
    for topic in local_settings.kafka_topics:
        if topic not in existing_topics:
            await kafka_client.create_topic(topic)  # Assuming create_topic is async
        else:
            logging.info(f"Topic '{topic}' already exists.")

    kafka_service_user = UserService(kafka_client, db_session)

    logging.info("KafkaConsumerService initialized successfully.")

    # Store the service in the app's state for global access
    fastapi_app.state.kafka_service = kafka_service_user
    yield


# Ensure the lifespan context is properly set
app.router.lifespan_context = lifespan


class HealthCheck(BaseModel):
    msg: str = "Hello world"


@app.get("/", response_model=HealthCheck, status_code=status.HTTP_200_OK)
async def get_health() -> HealthCheck:
    logging.info("Health check endpoint called")
    return HealthCheck()


@kafka_client.topic('user_request')
def consume_users(msg):
    try:
        logging.info(f"Consumed message in user_request: {msg}")
        kafka_service_user = get_kafka_service_user()
        kafka_service_user.save(msg)
    except Exception as e:
        logging.error(f"Error processing message in user_request: {e}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.webhook_host,
        port=app_settings.webhook_port,
        reload=app_settings.environment == 'dev'
    )

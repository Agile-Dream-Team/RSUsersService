import json
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel, ValidationError

from app.config.config import Settings
from app.utils.utils import TopicActionResponse
from kafka_rs.client import KafkaClient
from app.services.kafka_consumer_service import KafkaConsumerService


def configure_logging():
    logging.basicConfig(level=logging.INFO)


configure_logging()

app_settings = Settings()
app = FastAPI()

# Initialize KafkaClient using the singleton pattern
kafka_client = KafkaClient.instance(app_settings.kafka_bootstrap_servers, app_settings.kafka_group_id)


# Dependency to get the KafkaConsumerService instance
def get_kafka_service():
    return KafkaConsumerService(Settings(), kafka_client)


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

    kafka_service = KafkaConsumerService(local_settings, kafka_client)
    logging.info("KafkaConsumerService initialized successfully.")

    # Store the service in the app's state for global access
    fastapi_app.state.kafka_service = kafka_service

    try:
        yield  # Yield nothing or a suitable dictionary if needed
    finally:
        # Perform any cleanup if necessary
        logging.info("Cleaning up resources")


# Ensure the lifespan context is properly set
app.router.lifespan_context = lifespan


class HealthCheck(BaseModel):
    msg: str = "Hello world"


@app.get("/", response_model=HealthCheck, status_code=status.HTTP_200_OK)
async def get_health() -> HealthCheck:
    logging.info("Health check endpoint called")
    return HealthCheck()


@kafka_client.topic('get_all')
def consume_message_get_all(msg):
    try:
        data = msg.value().decode('utf-8')
        logging.info(f"Consumed message in get_all: {data}")
        kafka_service = get_kafka_service()
        kafka_service.get_all_service(data)
    except Exception as e:
        error = {"status_code": 400, "error": str(e)}
        sensor_data_json = json.dumps(error)
        kafka_client.send_message(TopicActionResponse.GET_ALL_RESPONSE, sensor_data_json)
        logging.error(f"Error processing message in get_all: {e}")


@kafka_client.topic('save')
def consume_message_save(msg):
    try:
        data = msg.value().decode('utf-8')
        logging.info(f"Consumed message in save: {data}")
        kafka_service = get_kafka_service()
        kafka_service.save_service(data)
    except Exception as e:
        error = {"status_code": 400, "error": str(e)}
        sensor_data_json = json.dumps(error)
        kafka_client.send_message(TopicActionResponse.SAVE_RESPONSE, sensor_data_json)
        logging.error(f"Error processing message in save: {e}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.webhook_host,
        port=app_settings.webhook_port,
        reload=app_settings.environment == 'dev'
    )

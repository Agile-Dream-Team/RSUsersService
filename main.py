import json
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel, ValidationError

from app.config.config import Settings
from app.config.database import setup_database
from app.services.camera_service import CameraService
from app.services.sensor_data_service import SensorDataService
from kafka_rs.client import KafkaClient


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
def get_kafka_service_sensor_data():
    return SensorDataService(kafka_client, db_session)


def get_kafka_service_camera():
    return CameraService(kafka_client, db_session)


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

    kafka_service_sensor_data = SensorDataService(kafka_client, db_session)
    kafka_service_camera = CameraService(kafka_client, db_session)

    logging.info("KafkaConsumerService initialized successfully.")

    # Store the service in the app's state for global access
    fastapi_app.state.kafka_service = kafka_service_sensor_data
    fastapi_app.state.kafka_service_camera = kafka_service_camera

    yield


# Ensure the lifespan context is properly set
app.router.lifespan_context = lifespan


class HealthCheck(BaseModel):
    msg: str = "Hello world"


@app.get("/", response_model=HealthCheck, status_code=status.HTTP_200_OK)
async def get_health() -> HealthCheck:
    logging.info("Health check endpoint called")
    return HealthCheck()


@kafka_client.topic('get_all_sensor_data')
def consume_message_get_all_sensor_data(msg):
    try:
        data = msg.value().decode('utf-8')
        logging.info(f"Consumed message in get_all_sensor_data: {data}")
        kafka_service_sensor_data = get_kafka_service_sensor_data()
        kafka_service_sensor_data.get_all_sensor_data_service(data)
    except Exception as e:
        error = {"status_code": 400, "error": str(e)}
        sensor_data_json = json.dumps(error)
        kafka_client.send_message("get_all_sensor_data_response", sensor_data_json)
        logging.error(f"Error processing message in get_all_sensor_data: {e}")


@kafka_client.topic('sensor_data')
def consume_message_save_sensor_data(msg):
    try:
        data = msg.value().decode('utf-8')
        logging.info(f"Consumed message in sensor_data: {data}")
        kafka_service_sensor_data = get_kafka_service_sensor_data()
        kafka_service_sensor_data.save_sensor_data_service(data)
    except Exception as e:
        error = {"status_code": 400, "error": str(e)}
        sensor_data_json = json.dumps(error)
        kafka_client.send_message("sensor_data_response", sensor_data_json)
        logging.error(f"Error processing message in sensor_data: {e}")


@kafka_client.topic('camera')
def consume_message_save_camera(msg):
    try:
        data = msg.value().decode('utf-8')
        logging.info(f"Consumed message in camera: {data}")
        kafka_service_camera = get_kafka_service_camera()
        kafka_service_camera.save_camera_service(data)
    except Exception as e:
        error = {"status_code": 400, "error": str(e)}
        camera_json = json.dumps(error)
        kafka_client.send_message("camera_response", camera_json)
        logging.error(f"Error processing message in camera: {e}")


@kafka_client.topic('get_all_camera')
def consume_message_get_all_camera(msg):
    try:
        data = msg.value().decode('utf-8')
        logging.info(f"Consumed message in get_all_camera: {data}")
        kafka_service_image = get_kafka_service_camera()
        kafka_service_image.get_all_camera_service(data)
    except Exception as e:
        error = {"status_code": 400, "error": str(e)}
        camera_json = json.dumps(error)
        kafka_client.send_message("get_all_camera_response", camera_json)
        logging.error(f"Error processing message in get_all_camera: {e}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.webhook_host,
        port=app_settings.webhook_port,
        reload=app_settings.environment == 'dev'
    )

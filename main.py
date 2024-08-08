# main.py
from fastapi import FastAPI, status
from pydantic import BaseModel
from app.api.v1.webhooks.webhook_routes import router as webhook_router
from app.config.kafka_manager import KafkaManager
import logging
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Read Kafka configuration from environment variables
kafka_host = os.getenv('KAFKA_HOST', 'localhost')
kafka_port = os.getenv('KAFKA_PORT', '9092')

# Initialize Kafka manager with retry parameters
"""
kafka_manager = KafkaManager(
    bootstrap_servers=f'{kafka_host}:{kafka_port}',
    topic='receiver',
    group_id='my_group',
)
"""


class HealthCheck(BaseModel):
    webhook_status: str = "OK"
    msg: str = "Hello world"


@app.get("/", response_model=HealthCheck, status_code=status.HTTP_200_OK)
async def get_health() -> HealthCheck:
    logging.info("Health check endpoint called")
    return HealthCheck()


# Include the webhook routes under /api/v1
app.include_router(webhook_router, prefix="/api/v1")

if __name__ == "__main__":
    webhook_host = os.getenv('WEBHOOK_HOST')
    webhook_port = int(os.getenv('WEBHOOK_PORT'))
    environment = os.getenv('ENVIRONMENT')
    reload = environment == 'dev'
    logging.info(f"Starting server at http://{webhook_host}:{webhook_port} with reload={reload}")
    uvicorn.run("main:app", host=webhook_host, port=webhook_port, reload=reload)
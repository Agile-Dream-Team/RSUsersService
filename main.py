# main.py
import logging
from fastapi import FastAPI, status, Depends
from pydantic import BaseModel, ValidationError
from contextlib import asynccontextmanager
import uvicorn

from app.api.v1.webhooks.webhook_routes import router as webhook_router
from app.config.config import Settings
from dependencies import startup_kafka_manager, has_access


def configure_logging():
    logging.basicConfig(level=logging.INFO)


class MainApp:
    def __init__(self):
        self.app_settings = Settings()
        self.app = FastAPI(lifespan=self.lifespan)
        configure_logging()
        self.include_routes()

    @asynccontextmanager
    async def lifespan(self, fastapi_app: FastAPI):
        try:
            local_settings = Settings()
        except ValidationError as e:
            logging.error(f"Environment variable validation error: {e}")
            raise

        startup_kafka_manager(fastapi_app, local_settings)
        kafka_manager = fastapi_app.state.kafka_manager
        logging.info(f"Creating Kafka topics: {local_settings.kafka_topics}")
        kafka_manager.create_kafka_topics(local_settings.kafka_topics)
        yield
        # TODO: Add any cleanup code here if needed

    def include_routes(self):
        self.app.include_router(webhook_router, prefix="/api/v1", dependencies=[Depends(has_access)])

    def run(self):
        logging.info(
            f"Starting server at ://{self.app_settings.webhook_host}:{self.app_settings.webhook_port} "
            f"with reload={self.app_settings.environment == 'dev'}"
        )
        uvicorn.run(
            "main:app",
            host=self.app_settings.webhook_host,
            port=self.app_settings.webhook_port,
            reload=self.app_settings.environment == 'dev'
        )


class HealthCheck(BaseModel):
    webhook_status: str = "OK"
    kafka_status: str = "Not implemented"
    msg: str = "Hello world"


app_instance = MainApp()
app = app_instance.app


@app.get("/", response_model=HealthCheck, status_code=status.HTTP_200_OK)
async def get_health() -> HealthCheck:
    logging.info("Health check endpoint called")
    # TODO: Implement Kafka health check
    return HealthCheck()


if __name__ == "__main__":
    app_instance.run()

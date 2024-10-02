from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    kafka_host: str = Field(..., env='KAFKA_HOST')
    kafka_port: str = Field(..., env='KAFKA_PORT')
    kafka_topics: list[str] = Field(..., env='KAFKA_TOPICS')
    kafka_group_id: str = Field(..., env='KAFKA_GROUP_ID')
    db_name: str = Field(..., env='DB_NAME')
    db_user: str = Field(..., env='DB_USER')
    db_password: str = Field(..., env='DB_PASSWORD')
    db_host: str = Field(..., env='DB_HOST')
    db_port: int = Field(..., env='DB_PORT')
    webhook_host: str = Field(..., env='WEBHOOK_HOST')
    webhook_port: int = Field(..., env='WEBHOOK_PORT')
    environment: str = Field(..., env='ENVIRONMENT')

    class Config:
        env_file = ".env"

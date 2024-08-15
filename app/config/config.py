from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str
    kafka_group_id: str
    kafka_topics: list[str]
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    kafka_host: str
    kafka_port: str
    environment: str

    class Config:
        env_file = ".env"

import logging
import psycopg2
from psycopg2 import sql
from confluent_kafka import Consumer, KafkaException, KafkaError
from contextlib import asynccontextmanager
import json
from app.dto.kafka_in_dto import KafkaInDTO, KafkaInDataDTO

from pydantic import ValidationError
from contextlib import contextmanager
from app.config.config import Settings
from app.services.kafka_consumer_service import KafkaConsumerService
from dependencies import startup_kafka_manager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.domain.sensor_data import Base


def configure_logging():
    logging.basicConfig(level=logging.INFO)


class Database:
    def __init__(self, settings: Settings):
        try:
            self.connection = psycopg2.connect(
                dbname=settings.db_name,
                user=settings.db_user,
                password=settings.db_password,
                host=settings.db_host,
                port=settings.db_port
            )
            self.cursor = self.connection.cursor()
            logging.info("Postgres connection established successfully.")
        except psycopg2.Error as e:
            logging.error(f"Failed to connect to Postgres: {e}")
            raise

    def execute_query(self, query: str):
        self.cursor.execute(query)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


class KafkaConsumer:
    def __init__(self, settings: Settings):
        self.consumer = Consumer({
            'bootstrap.servers': settings.kafka_bootstrap_servers,
            'group.id': settings.kafka_group_id,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe(settings.kafka_topics)

        # Database setup
        engine = create_engine(
            f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.db_session = Session()

        self.consumer_service = KafkaConsumerService(self.db_session)

    def consume_messages(self):
        while True:
            try:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError.PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())
                logging.info(f"Consumed message from topic {msg.topic()}: {msg.value().decode('utf-8')}")

                # Parse the message into KafkaInDTO
                try:
                    message_data = json.loads(msg.value().decode('utf-8'))
                    kafka_in_dto = KafkaInDTO(**message_data)
                    logging.info(f"Parsed message: {kafka_in_dto}")

                    # Process the message using KafkaConsumerService
                    self.consumer_service.process_message(kafka_in_dto)
                except (json.JSONDecodeError, ValidationError) as e:
                    logging.error(f"Failed to parse message: {e}")
            except Exception as e:
                logging.error(f"Error in consume_messages: {e}")


class MainApp:
    def __init__(self):
        self.app_settings = Settings()
        configure_logging()

    @contextmanager
    def lifespan(self):
        try:
            local_settings = Settings()
        except ValidationError as e:
            logging.error(f"Environment variable validation error: {e}")
            raise

        startup_kafka_manager(local_settings)
        kafka_manager = KafkaConsumer(local_settings)
        kafka_manager.consume_messages()
        yield
        # TODO: Add any cleanup code here if needed

    def run(self):
        logging.info("Starting application")
        with self.lifespan():
            pass


if __name__ == "__main__":
    app_instance = MainApp()
    app_instance.run()

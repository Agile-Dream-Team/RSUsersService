import logging
import psycopg2
from confluent_kafka import Consumer, KafkaException, KafkaError
import json
from app.dto.kafka_in_dto import KafkaInDTO, KafkaGetAllDTO, KafkaGetByIdDTO
from pydantic import ValidationError
from contextlib import contextmanager
from app.config.config import Settings
from app.services.kafka_consumer_service import KafkaConsumerService
from app.utils.utils import EventActionConsume
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


def kafka_topic(topic_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            instance = args[0]
            instance.consumer.subscribe([topic_name])
            return func(*args, **kwargs)

        return wrapper

    return decorator


def setup_database(settings):
    engine = create_engine(
        f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


class KafkaConsumer:
    def __init__(self, settings: Settings):
        self.consumer = Consumer({
            'bootstrap.servers': settings.kafka_bootstrap_servers,
            'group.id': settings.kafka_group_id,
            'auto.offset.reset': 'earliest'
        })
        self.db_session = setup_database(settings)
        self.consumer_service = KafkaConsumerService(self.db_session, settings.kafka_bootstrap_servers)

    def consume_message(self, topic_name):
        while True:
            try:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())
                logging.info(f"Consumed message from topic {msg.topic()}: {msg.value().decode('utf-8')}")

                # Parse the message into the appropriate DTO
                try:
                    message_data = json.loads(msg.value().decode('utf-8'))
                    event_type = message_data.get('event')

                    if event_type == EventActionConsume.CREATE:
                        kafka_in_dto = KafkaInDTO(**message_data)
                    elif event_type == EventActionConsume.GET_ALL:
                        kafka_in_dto = KafkaGetAllDTO(**message_data)
                    elif event_type == EventActionConsume.GET_BY_ID:
                        kafka_in_dto = KafkaGetByIdDTO(**message_data)
                    else:
                        logging.warning(f"Unhandled event type: {event_type}")
                        continue

                    # Process the message using KafkaConsumerService
                    self.consumer_service.process_message(kafka_in_dto)
                except (json.JSONDecodeError, ValidationError) as e:
                    logging.error(f"Failed to parse message: {e}")
            except Exception as e:
                logging.error(f"Error in consume_message for topic {topic_name}: {e}")

    @kafka_topic('get_all')
    def consume_get_all_messages(self):
        self.consume_message('get_all')

    @kafka_topic('create')
    def consume_create_messages(self):
        self.consume_message('create')

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
        kafka_manager.consume_get_all_messages()
        yield

    def run(self):
        logging.info("Starting application")
        with self.lifespan():
            pass


if __name__ == "__main__":
    app_instance = MainApp()
    app_instance.run()

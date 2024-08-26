import json
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from app.config.config import Settings
from app.domain.sensor_data import Base
from app.exceptions.custom_exceptions import BadRequestException
from app.mapper.sensor_data_mapper import dto_to_entity
from app.repository.sensor_data_repository import SensorDataRepository
from app.utils.utils import TopicActionResponse
from kafka_rs.client import KafkaClient


class Database:
    def __init__(self, settings: Settings):
        self.engine = create_engine(
            f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}",
            pool_pre_ping=True,
            echo_pool=True,
            pool_size=10,
            max_overflow=20
        )
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def get_session(self):
        return self.Session()

    def close(self):
        self.Session.remove()


def setup_database(settings: Settings):
    db = Database(settings)
    Base.metadata.create_all(db.engine)
    return db.get_session()


class KafkaConsumerService:
    def __init__(self, settings: Settings, kafka_client: KafkaClient):
        self.settings = settings
        self.kafka_client = kafka_client
        self.db = Database(self.settings)
        self.db_session = self.db.get_session()
        self.sensor_data_repository = SensorDataRepository(self.db_session)

    def get_all_service(self, kafka_in_dto):
        try:
            #TODO: implement error handling to be sent to Kafka

            logging.info(f"Processing message: {kafka_in_dto}")
            sensor_data = self.sensor_data_repository.get_all()
            logging.info(f"Retrieved sensor data: {sensor_data}")
            sensor_data_json = json.dumps([data.to_dict() for data in sensor_data])
            self.kafka_client.send_message(TopicActionResponse.GET_ALL_RESPONSE, sensor_data_json)
        except SQLAlchemyError as e:
            logging.error(f"Database error processing message: {e}")
            self.db_session.rollback()
            raise BadRequestException(f"Failed to process message: {e}")
        finally:
            self.db_session.close()

    def save_service(self, kafka_in_dto):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")
            sensor_data = dto_to_entity(kafka_in_dto)
            self.sensor_data_repository.save(sensor_data)
            sensor_data_dict = sensor_data.to_dict()
            sensor_data_dict["status_code"] = 200
            sensor_data_json = json.dumps(sensor_data_dict)
            self.kafka_client.send_message(TopicActionResponse.SAVE_RESPONSE, sensor_data_json)
            return sensor_data
        except SQLAlchemyError as e:
            self.db_session.rollback()
            error = {"status_code": 400, "error": str(e)}
            sensor_data_json = json.dumps(error)
            self.kafka_client.send_message(TopicActionResponse.SAVE_RESPONSE, sensor_data_json)
            raise BadRequestException(f"Failed to process message: {e}")
        finally:
            self.db_session.close()

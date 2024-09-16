import json
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.custom_exceptions import BadRequestException
from app.mapper.sensor_data_mapper import dto_to_entity
from app.repository.sensor_data_repository import SensorDataRepository
from kafka_rs.client import KafkaClient


class SensorDataService:
    def __init__(self, kafka_client: KafkaClient, db_session):
        self.kafka_client = kafka_client
        self.db_session = db_session
        self.sensor_data_repository = SensorDataRepository(self.db_session)

    def get_all_sensor_data_service(self, kafka_in_dto):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")
            sensor_data = self.sensor_data_repository.get_all()
            logging.info(f"Retrieved sensor data: {sensor_data}")
            sensor_data_json = json.dumps([data.to_dict() for data in sensor_data])
            self.kafka_client.send_message("get_all_sensor_data_response", sensor_data_json)
        except SQLAlchemyError as e:
            logging.error(f"Database error processing message: {e}")
            self.db_session.rollback()
            raise BadRequestException(f"Failed to process message: {e}")
        finally:
            self.db_session.close()

    def save_sensor_data_service(self, kafka_in_dto):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")
            sensor_data = dto_to_entity(kafka_in_dto)
            self.sensor_data_repository.save(sensor_data)
            sensor_data_dict = sensor_data.to_dict()
            sensor_data_dict["status_code"] = 200
            sensor_data_json = json.dumps(sensor_data_dict)
            self.kafka_client.send_message("sensor_data_response", sensor_data_json)
            return sensor_data
        except SQLAlchemyError as e:
            self.db_session.rollback()
            error = {"status_code": 400, "error": str(e)}
            sensor_data_json = json.dumps(error)
            self.kafka_client.send_message("sensor_data_response", sensor_data_json)
            raise BadRequestException(f"Failed to process message: {e}")
        finally:
            self.db_session.close()
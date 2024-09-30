import json
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.custom_exceptions import BadRequestException
from app.mapper.sensor_data_mapper import dto_to_entity
from app.repository.sensor_data_repository import SensorDataRepository
from RSKafkaWrapper.client import KafkaClient
from RSErrorHandler.ErrorHandler import RSKafkaException


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
            sensor_data_json = [data.to_dict() for data in sensor_data]

            sensor_data_dict = {"sensor_data": sensor_data_json}

            self.kafka_client.send_message("get_all_sensor_data_response", sensor_data_dict)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RSKafkaException(f"Database error: {e}", self.kafka_client, "get_all_sensor_data_response")
        finally:
            self.db_session.close()

    def save_sensor_data_service(self, kafka_in_dto):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")
            sensor_data = dto_to_entity(kafka_in_dto)
            self.sensor_data_repository.save(sensor_data)
            sensor_data_dict = sensor_data.to_dict()
            sensor_data_dict.update({"status_code": 200})
            self.kafka_client.send_message("sensor_data_response", sensor_data_dict)
            return sensor_data
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RSKafkaException(f"Database error: {e}", self.kafka_client, "sensor_data_response")

        finally:
            self.db_session.close()

    def get_by_id_sensor_data_service(self, kafka_in_dto):
        try:
            record_id = kafka_in_dto['id']

            sensor_data = self.sensor_data_repository.get_by_id(record_id)
            logging.info(f"Retrieved sensor data: {sensor_data}")
            sensor_data_dict = sensor_data.to_dict() if sensor_data else {}
            self.kafka_client.send_message("get_by_id_sensor_data_response", sensor_data_dict)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RSKafkaException(f"Database error: {e}", self.kafka_client, "get_by_id_sensor_data_response")

        finally:
            self.db_session.close()

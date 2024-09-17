import json
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.custom_exceptions import BadRequestException
from app.mapper.camera_mapper import dto_to_entity
from app.repository.camera_repository import CameraRepository
from kafka_rs.client import KafkaClient


class CameraService:
    def __init__(self, kafka_client: KafkaClient, db_session):
        self.kafka_client = kafka_client
        self.db_session = db_session
        self.camera_repository = CameraRepository(self.db_session)

    def get_all_camera_service(self, kafka_in_dto):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")
            camera = self.camera_repository.get_all()
            logging.info(f"Retrieved camera: {camera}")
            camera_json = json.dumps([data.to_dict() for data in camera])
            self.kafka_client.send_message("get_all_camera_response", camera_json)
        except SQLAlchemyError as e:
            logging.error(f"Database error processing message: {e}")
            self.db_session.rollback()
            raise BadRequestException(f"Failed to process message: {e}")
        finally:
            self.db_session.close()

    def save_camera_service(self, kafka_in_dto):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")
            image = dto_to_entity(kafka_in_dto)
            self.camera_repository.save(image)
            sensor_data_dict = image.to_dict()
            sensor_data_dict["status_code"] = 200
            sensor_data_json = json.dumps(sensor_data_dict)
            self.kafka_client.send_message("camera_response", sensor_data_json)
            return image
        except SQLAlchemyError as e:
            self.db_session.rollback()
            error = {"status_code": 400, "error": str(e)}
            sensor_data_json = json.dumps(error)
            self.kafka_client.send_message("camera_response", sensor_data_json)
            raise BadRequestException(f"Failed to process message: {e}")
        finally:
            self.db_session.close()

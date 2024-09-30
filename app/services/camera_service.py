import logging
from sqlalchemy.exc import SQLAlchemyError

from RSErrorHandler.ErrorHandler import RSKafkaException
from app.mapper.camera_mapper import dto_to_entity
from app.repository.camera_repository import CameraRepository
from RSKafkaWrapper.client import KafkaClient


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
            camera_json = [data.to_dict() for data in camera]
            logging.info(f'type of camera_json: {type(camera_json)}')
            camera_dict = {"cameras": camera_json}

            self.kafka_client.send_message("get_all_camera_response", camera_dict)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RSKafkaException(f"Database error: {e}", self.kafka_client, "get_all_camera_response")

        finally:
            self.db_session.close()

    def save_camera_service(self, kafka_in_dto):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")
            image = dto_to_entity(kafka_in_dto)
            self.camera_repository.save(image)
            camera_dict = image.to_dict()
            camera_dict.update({"status_code": 200})
            self.kafka_client.send_message("camera_response", camera_dict)
            return image
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RSKafkaException(f"Database error: {e}", self.kafka_client, "camera_response")

        finally:
            self.db_session.close()

    def get_by_id_camera_service(self, kafka_in_dto):
        try:
            record_id = kafka_in_dto['id']
            camera = self.camera_repository.get_by_id(record_id)
            logging.info(f"Retrieved camera: {camera}")
            camera_dict = camera.to_dict() if camera else {}
            self.kafka_client.send_message("get_by_id_camera_response", camera_dict)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RSKafkaException(f"Database error: {e}", self.kafka_client, "get_by_id_camera_response")

        finally:
            self.db_session.close()

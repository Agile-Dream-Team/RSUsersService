import logging
from sqlalchemy.exc import SQLAlchemyError
from app.mapper.user_mapper import dto_to_entity
from RSKafkaWrapper.client import KafkaClient
from RSErrorHandler.ErrorHandler import RSKafkaException
from app.repository.user_repository import UserRepository


class UserService:
    def __init__(self, kafka_client: KafkaClient, db_session):
        self.kafka_client = kafka_client
        self.db_session = db_session
        self.user_repository = UserRepository(self.db_session)

    def get_all(self, kafka_in_dto):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")
            sensor_data = self.user_repository.get_all()
            sensor_data_json = [data.to_dict() for data in sensor_data]

            sensor_data_dict = {"sensor_data": sensor_data_json}

            self.kafka_client.send_message("get_all_sensor_data_response", sensor_data_dict)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RSKafkaException(f"Database error: {e}", self.kafka_client, "user")
        finally:
            self.db_session.close()

    def save(self, kafka_in_dto):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")
            user = dto_to_entity(kafka_in_dto)
            self.user_repository.save(user)
            user_dict = user.to_dict()
            user_dict.update({"status_code": 200})
            self.kafka_client.send_message("user_response", user_dict)
            return user
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RSKafkaException(f"Database error: {e}", self.kafka_client, "user_response")

        finally:
            self.db_session.close()

    def get_by_id(self, kafka_in_dto):
        try:
            record_id = kafka_in_dto['id']

            user = self.user_repository.get_by_id(record_id)
            logging.info(f"Retrieved sensor data: {user}")
            sensor_data_dict = user.to_dict() if user else {}
            self.kafka_client.send_message("get_by_id_sensor_data_response", sensor_data_dict)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RSKafkaException(f"Database error: {e}", self.kafka_client, "get_by_id_sensor_data_response")

        finally:
            self.db_session.close()

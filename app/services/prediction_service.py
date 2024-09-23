# app/services/prediction_service.py
import logging
from sqlalchemy.exc import SQLAlchemyError

from RSErrorHandler.ErrorHandler import RSKafkaException
from app.repository.prediction_repository import PredictionRepository
from RSKafkaWrapper.client import KafkaClient
from app.domain.prediction import Prediction


class PredictionService:
    def __init__(self, kafka_client: KafkaClient, db_session):
        self.kafka_client = kafka_client
        self.db_session = db_session
        self.prediction_repository = PredictionRepository(self.db_session)

    def get_prediction_service(self, kafka_in_dto):
        try:
            record_id = kafka_in_dto['id']

            prediction = self.prediction_repository.get_constructed_data(record_id)
            logging.info(f"Retrieved prediction construction: {prediction}")
            prediction_dict = prediction.to_dict() if prediction else {}
            logging.info(f'prediction_dict: {prediction_dict}')
            self.kafka_client.send_message(["prediction_response", "prediction_ai_service_request"], prediction_dict)
            #self.kafka_client.send_message("prediction_ai_service_request", prediction_dict)

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RSKafkaException(f"Database error: {e}", self.kafka_client, "prediction_response")

        finally:
            self.db_session.close()

from sqlalchemy.orm import Session
from app.dto.kafka_in_dto import KafkaInDTO
from app.utils.utils import EventType
from app.services.kafka_producer_service import KafkaProducerService
from app.exceptions.custom_exceptions import BadRequestException
from app.mapper.sensor_data_mapper import map_dto_to_entity
from app.repository.sensor_data_repository import SensorDataRepository
import logging


class KafkaConsumerService:
    def __init__(self, db_session: Session):
        self.producer_service = KafkaProducerService()
        self.sensor_data_repository = SensorDataRepository(db_session)

    def process_message(self, kafka_in_dto: KafkaInDTO):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")
            if kafka_in_dto.event == EventType.NORMAL:
                logging.info(f"Processing event: {kafka_in_dto.event}")
                sensor_data = map_dto_to_entity(kafka_in_dto)
                self.sensor_data_repository.save(sensor_data)
            else:
                logging.warning(f"Unhandled event type: {kafka_in_dto.event}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            raise BadRequestException(f"Failed to process message: {e}")

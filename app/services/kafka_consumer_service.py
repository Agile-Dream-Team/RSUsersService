import logging

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import BadRequestException
from app.mapper.sensor_data_mapper import map_dto_to_entity
from app.repository.sensor_data_repository import SensorDataRepository
from app.services.kafka_producer_service import KafkaProducerService
from app.utils.utils import EventActionConsume


class KafkaConsumerService:
    def __init__(self, db_session: Session, kafka_bootstrap_servers: str):
        self.producer_service = KafkaProducerService(kafka_bootstrap_servers)
        self.sensor_data_repository = SensorDataRepository(db_session)

    def process_message(self, kafka_in_dto):
        try:
            logging.info(f"Processing message: {kafka_in_dto}")

            match kafka_in_dto.event:
                case EventActionConsume.CREATE:
                    logging.info(f"Processing event: {kafka_in_dto.event}")
                    sensor_data = map_dto_to_entity(kafka_in_dto)
                    self.sensor_data_repository.save(sensor_data)

                case EventActionConsume.GET_ALL:
                    logging.info(f"Processing event: {kafka_in_dto.event}")
                    sensor_data = self.sensor_data_repository.get_all()
                    logging.info(f"Retrieved sensor data: {sensor_data}")
                    self.producer_service.get_all_produce(sensor_data)

                case EventActionConsume.GET_BY_ID:
                    logging.info(f"Processing event: {kafka_in_dto.event}")
                    sensor_data = self.sensor_data_repository.get_by_id(kafka_in_dto.uuid)
                    self.producer_service.get_by_id_produce(sensor_data)

                case _:
                    logging.warning(f"Unhandled event type: {kafka_in_dto.event}")

        except Exception as e:
            logging.error(f"Error processing message: {e}")
            raise BadRequestException(f"Failed to process message: {e}")
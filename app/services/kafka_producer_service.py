import logging
from ..config.kafka_manager import KafkaManager
from ..dto.kafka_out_dto import KafkaOutDTO
from ..dto.webhook_in_dto import WebhookDTO
from confluent_kafka import KafkaException


class KafkaProducerService:
    def __init__(self, kafka_manager: KafkaManager):
        self.producer = kafka_manager.producer
        self.topic = kafka_manager.topics
        logging.basicConfig(level=logging.INFO)

    def process_webhook_to_kafka(self, webhook_dto: WebhookDTO):
        try:
            kafka_out_dto = KafkaOutDTO(
                data=webhook_dto.data.dict(),
                source="webhook"
            )
            logging.info(f"Sending message to Kafka: {kafka_out_dto.json()}")

            self.producer.produce(webhook_dto.event, value=kafka_out_dto.json())
            self.producer.flush()
        except KafkaException as e:
            logging.error(f"Failed to send message: {e}")
            raise

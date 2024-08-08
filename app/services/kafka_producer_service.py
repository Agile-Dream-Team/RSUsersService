# app/services/kafka_producer_service.py
from app.config.kafka import KafkaConfig
from app.dto.kafka_out_dto import KafkaOutDTO
from app.dto.webhook_in_dto import WebhookDTO


class KafkaProducerService:
    def __init__(self, kafka_config: KafkaConfig):
        self.producer = kafka_config.create_producer()
        self.topic = kafka_config.topic

    def send_to_kafka(self, webhook_dto: WebhookDTO):
        kafka_out_dto = KafkaOutDTO(
            event=webhook_dto.event,
            data=webhook_dto.data,
            source="webhook"
        )
        self.producer.produce(self.topic, key=kafka_out_dto.event, value=kafka_out_dto.json())
        self.producer.flush()

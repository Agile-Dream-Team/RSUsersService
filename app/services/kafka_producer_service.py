import json
from confluent_kafka import Producer
import logging

from app.utils.utils import EventActionProduce


class KafkaProducerService:
    def __init__(self, kafka_bootstrap_servers: str):
        self.producer = Producer({'bootstrap.servers': kafka_bootstrap_servers})

    def get_all_produce(self, sensor_data):
        try:
            # Serialize sensor data to JSON
            sensor_data_json = json.dumps([data.to_dict() for data in sensor_data])

            # Send the serialized data to a Kafka topic
            self.producer.produce(EventActionProduce.GET_ALL_PRODUCE, sensor_data_json)
            self.producer.flush()

            logging.info(f"Sent sensor data to Kafka: {sensor_data_json} to topic: {EventActionProduce.GET_ALL_PRODUCE}")
        except Exception as e:
            logging.error(f"Failed to send sensor data: {e}")
            raise e

    def get_by_id_produce(self, sensor_data):
        pass

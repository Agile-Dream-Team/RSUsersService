# app/config/kafka.py
from confluent_kafka import Producer, Consumer

class KafkaConfig:
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id

    def get_producer_config(self):
        return {
            'bootstrap.servers': self.bootstrap_servers
        }

    def get_consumer_config(self):
        return {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        }

    def create_producer(self):
        return Producer(self.get_producer_config())

    def create_consumer(self):
        return Consumer(self.get_consumer_config())
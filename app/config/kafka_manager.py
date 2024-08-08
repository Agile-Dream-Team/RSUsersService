# app/config/kafka_manager.py
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient
import logging


class KafkaManager:
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.producer = self.create_producer()
        self.consumer = self.create_consumer()

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

    def check_broker_status(self):
        admin_client = AdminClient({'bootstrap.servers': self.bootstrap_servers})
        logging.info('Checking Kafka broker status...')
        try:
            cluster_metadata = admin_client.list_topics(timeout=10)
            return {
                'brokers': cluster_metadata.brokers,
                'topics': cluster_metadata.topics
            }
        except Exception as e:
            logging.error(f'Connection failed: {str(e)}')
            return {'error': 'KafkaError', 'str': str(e)}

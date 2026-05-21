import os
import pika
import logging

logger = logging.getLogger(__name__)

QUEUE_NAME = "notifications"

def create_connection():
    credentials = pika.PlainCredentials(
        os.getenv('RABBITMQ_USER'),
        os.getenv('RABBITMQ_PASSWORD')
    )
    parameters = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST'),
        port=int(os.getenv('RABBITMQ_PORT', 5672)),
        virtual_host=os.getenv('RABBITMQ_VHOST', '/'),
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300
    )
    return pika.BlockingConnection(parameters)
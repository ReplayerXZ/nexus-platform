import os
import pika
import logging

logger = logging.getLogger(__name__)

connection = None
channel = None

QUEUE_NAME = "notifications"

def connect_rabbitmq():
    global connection, channel
    try:
        credentials = pika.PlainCredentials(
            os.getenv('RABBITMQ_USER'),
            os.getenv('RABBITMQ_PASSWORD')
        )
        parameters = pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST'),
            port=int(os.getenv('RABBITMQ_PORT', 5672)),
            virtual_host=os.getenv('RABBITMQ_VHOST', '/'),
            credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        logger.info("✅ RabbitMQ connected")
    except Exception as e:
        logger.error(f"❌ RabbitMQ connection failed: {e}")
        raise

def get_channel():
    return channel

def publish_message(message: str):
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
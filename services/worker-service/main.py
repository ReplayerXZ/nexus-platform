import os
import time
import logging
from dotenv import load_dotenv
from app.config.db import connect_db
from app.config.rabbitmq import create_connection, QUEUE_NAME
from app.processors.notification_processor import process_notification

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def start_worker():
    logger.info("🚀 Worker service starting...")

    # Koneksi ke MongoDB
    connect_db()

    # Retry koneksi RabbitMQ dengan backoff
    max_retries = 10
    for attempt in range(max_retries):
        try:
            connection = create_connection()
            channel = connection.channel()

            # Pastikan queue ada
            channel.queue_declare(queue=QUEUE_NAME, durable=True)

            # Proses 1 pesan per satu waktu (fair dispatch)
            channel.basic_qos(prefetch_count=1)

            # Daftarkan callback processor
            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=process_notification
            )

            logger.info(f"✅ Worker siap — mendengarkan queue: {QUEUE_NAME}")
            logger.info("⏳ Menunggu pesan... (Ctrl+C untuk berhenti)")

            # Mulai consume — blocking sampai dihentikan
            channel.start_consuming()

        except KeyboardInterrupt:
            logger.info("🛑 Worker dihentikan")
            break
        except Exception as e:
            wait = 5 * (attempt + 1)
            logger.error(f"❌ Koneksi gagal (attempt {attempt + 1}/{max_retries}): {e}")
            logger.info(f"⏳ Retry dalam {wait} detik...")
            time.sleep(wait)

    logger.info("Worker service stopped")

if __name__ == '__main__':
    start_worker()
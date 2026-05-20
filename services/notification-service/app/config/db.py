import os
import logging
from pymongo import MongoClient

logger = logging.getLogger(__name__)
client = None
db = None

def connect_db():
    global client, db
    try:
        uri = (
            f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}"
            f"@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}"
            f"/{os.getenv('MONGO_DB')}?authSource=admin"
        )
        client = MongoClient(uri)
        db = client[os.getenv('MONGO_DB')]
        # Ping untuk verifikasi koneksi
        client.admin.command('ping')
        logger.info("✅ MongoDB connected")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        raise

def get_db():
    return db

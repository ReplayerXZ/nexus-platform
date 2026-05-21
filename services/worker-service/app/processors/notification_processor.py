import json
import logging
from datetime import datetime
from bson import ObjectId
from app.config.db import get_db

logger = logging.getLogger(__name__)

def process_notification(channel, method, properties, body):
    """
    Callback yang dipanggil setiap ada pesan baru di queue.
    """
    try:
        # Parse pesan dari queue
        data = json.loads(body.decode('utf-8'))
        notification_id = data.get('notification_id')
        notif_type = data.get('type')
        title = data.get('title')
        message = data.get('message')
        user_id = data.get('user_id')

        logger.info(f"📨 Processing notification {notification_id} type={notif_type}")

        # Simulasi proses pengiriman berdasarkan type
        success = False

        if notif_type == 'email':
            success = _send_email(user_id, title, message)
        elif notif_type == 'push':
            success = _send_push(user_id, title, message)
        elif notif_type == 'sms':
            success = _send_sms(user_id, message)
        else:
            logger.warning(f"Unknown notification type: {notif_type}")
            success = False

        # Update status di MongoDB
        new_status = "sent" if success else "failed"
        _update_status(notification_id, new_status)

        # Acknowledge pesan — beritahu RabbitMQ bahwa pesan sudah diproses
        channel.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"✅ Notification {notification_id} processed → status: {new_status}")

    except Exception as e:
        logger.error(f"❌ Error processing notification: {e}")
        # Nack — kembalikan pesan ke queue untuk diproses ulang
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def _send_email(user_id: str, title: str, message: str) -> bool:
    """Simulasi kirim email"""
    logger.info(f"📧 Sending email to user {user_id}: {title}")
    # Di production: integrasi dengan SMTP / SendGrid / Mailgun
    return True

def _send_push(user_id: str, title: str, message: str) -> bool:
    """Simulasi kirim push notification"""
    logger.info(f"🔔 Sending push to user {user_id}: {title}")
    # Di production: integrasi dengan FCM / APNs
    return True

def _send_sms(user_id: str, message: str) -> bool:
    """Simulasi kirim SMS"""
    logger.info(f"📱 Sending SMS to user {user_id}: {message}")
    # Di production: integrasi dengan Twilio / Vonage
    return True

def _update_status(notification_id: str, status: str):
    """Update status notifikasi di MongoDB"""
    try:
        db = get_db()
        db.notifications.update_one(
            {"_id": ObjectId(notification_id)},
            {"$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            }}
        )
        logger.info(f"📝 Status updated: {notification_id} → {status}")
    except Exception as e:
        logger.error(f"❌ Failed to update status: {e}")
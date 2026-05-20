import json
import logging
from datetime import datetime
from bson import ObjectId
from flask import request, jsonify
from app.config.db import get_db
from app.config.rabbitmq import publish_message

logger = logging.getLogger(__name__)

def serialize(doc):
    """Convert MongoDB document ke JSON-serializable dict"""
    doc['_id'] = str(doc['_id'])
    if 'created_at' in doc:
        doc['created_at'] = doc['created_at'].isoformat()
    if 'updated_at' in doc:
        doc['updated_at'] = doc['updated_at'].isoformat()
    return doc

def send_notification():
    """POST /notifications/send"""
    data = request.get_json()

    required = ['user_id', 'type', 'title', 'message']
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} wajib diisi"}), 400

    valid_types = ['email', 'push', 'sms']
    if data['type'] not in valid_types:
        return jsonify({"error": f"type harus salah satu dari {valid_types}"}), 400

    try:
        db = get_db()

        # Simpan ke MongoDB
        notification = {
            "user_id": data['user_id'],
            "type": data['type'],
            "title": data['title'],
            "message": data['message'],
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = db.notifications.insert_one(notification)
        notification_id = str(result.inserted_id)

        # Publish ke RabbitMQ untuk diproses worker
        payload = json.dumps({
            "notification_id": notification_id,
            "user_id": data['user_id'],
            "type": data['type'],
            "title": data['title'],
            "message": data['message']
        })
        publish_message(payload)

        logger.info(f"Notification {notification_id} published to queue")
        return jsonify({
            "message": "Notifikasi berhasil dikirim ke queue",
            "notification_id": notification_id
        }), 201

    except Exception as e:
        logger.error(f"Send notification error: {e}")
        return jsonify({"error": "Internal server error"}), 500

def get_notifications():
    """GET /notifications?user_id=xxx"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id wajib diisi"}), 400

    try:
        db = get_db()
        query = {"user_id": user_id}

        # Filter by status jika ada
        status = request.args.get('status')
        if status:
            query['status'] = status

        notifications = list(
            db.notifications.find(query).sort("created_at", -1).limit(50)
        )
        notifications = [serialize(n) for n in notifications]

        return jsonify({
            "notifications": notifications,
            "total": len(notifications)
        }), 200

    except Exception as e:
        logger.error(f"Get notifications error: {e}")
        return jsonify({"error": "Internal server error"}), 500

def get_notification_by_id(notification_id: str):
    """GET /notifications/:id"""
    try:
        db = get_db()
        notification = db.notifications.find_one({"_id": ObjectId(notification_id)})
        if not notification:
            return jsonify({"error": "Notifikasi tidak ditemukan"}), 404

        return jsonify({"notification": serialize(notification)}), 200

    except Exception as e:
        logger.error(f"Get notification by id error: {e}")
        return jsonify({"error": "Internal server error"}), 500
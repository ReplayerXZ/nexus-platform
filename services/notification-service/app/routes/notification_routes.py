from flask import Blueprint
from app.controllers.notification_controller import (
    send_notification,
    get_notifications,
    get_notification_by_id
)

notification_bp = Blueprint('notifications', __name__)

notification_bp.post('/send')(send_notification)
notification_bp.get('/')(get_notifications)
notification_bp.get('/<notification_id>')(get_notification_by_id)
from datetime import datetime

def create_notification(user_id: str, type: str, title: str, message: str, status: str = "pending"):
    return {
        "user_id": user_id,
        "type": type,
        "title": title,
        "message": message,
        "status": status,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
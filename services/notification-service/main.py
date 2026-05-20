import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.config.db import connect_db
from app.config.rabbitmq import connect_rabbitmq
from app.routes.notification_routes import notification_bp

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Koneksi ke database dan message queue
    connect_db()
    connect_rabbitmq()

    # Register blueprint
    app.register_blueprint(notification_bp, url_prefix='/notifications')

    @app.get('/health')
    def health():
        return {
            "status": "ok",
            "service": "notification-service",
        }

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Route tidak ditemukan"}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {"error": "Internal server error"}, 500

    return app

if __name__ == '__main__':
    port = int(os.getenv('NOTIFICATION_PORT', 5001))
    app = create_app()
    logger.info(f"🚀 Notification service berjalan di port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
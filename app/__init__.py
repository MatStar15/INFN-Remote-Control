from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from celery import Celery
import os


# Initialize extensions
db = SQLAlchemy()

socketio = SocketIO()

def get_socketio():
    return SocketIO(message_queue=os.environ.get('SOCKETIO_MESSAGE_QUEUE', 'redis://'),)


celery = Celery()


def create_app(config_name='development'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    # Initialize extensions with app
    db.init_app(app)
    socketio.init_app(app,
                      message_queue=os.environ.get('SOCKETIO_MESSAGE_QUEUE', 'redis://'),
                      cors_allowed_origins="*",
                      logger=True,
                      engineio_logger=True,
                      ping_timeout=300,
                      ping_interval=60,
                      asyn_mode='threading'
                      )

    from . import emitters, events

    global celery
    celery = Celery(app.import_name)
    celery.conf.update(app.config)

    conn = celery.connection()
    conn.connect()
    print("Successfully connected to Celery broker")


    # Register blueprints
    from .routes.main import main as main_blueprint
    from .routes.api import api as api_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Setup database
    with app.app_context():
        db.create_all()

    # Create file watcher
    from app.tasks.file_watcher import setup_file_watcher
    with app.app_context():
        setup_file_watcher(app)


    return app
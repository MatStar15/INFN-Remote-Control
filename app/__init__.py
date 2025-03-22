from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from celery import Celery
import os, logging

# TODO: only start one calculation at a time
# TODO: update job status and number of files on the dashboard page
# TODO: Get a command line instead of a form for the calculation

# Initialize extensions
db = SQLAlchemy()
socketio = SocketIO()
celery = None
app = None

def get_socketio():
    return SocketIO(message_queue=os.environ.get('SOCKETIO_MESSAGE_QUEUE', 'redis://'),)

def create_app(config_name='development'):
    global app
    if app:
        return app

    app = Flask(__name__)
    # Load configuration
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    global celery

    # Initialize extensions with app
    db.init_app(app)
    socketio.init_app(app,
                      message_queue=app.config.get('SOCKETIO_MESSAGE_QUEUE', 'redis://'),
                      ping_timeout=30,
                      ping_interval=5,
                      cors_allowed_origins="*",
                      async_mode='threading',
                      reconnection=True,
                      reconnection_attempts=3,
                      reconnection_delay=500,
                      # logger=True,
                      # engineio_logger=True,
                      )


    from . import emitters, events

    # Initialize Celery once
    if not celery:
        celery = Celery()
        celery.config_from_object(f'config.{config_name.capitalize()}Config')
        # logging.warning("Celery Tasks: " + str(celery.tasks))

        # Only start worker if not in debug mode and main process
        if not app.debug:
            worker = celery.Worker(
                # pool='solo',
                concurrency=1,
                loglevel='INFO',
                # hostname=unique_hostname,
            )
            from threading import Thread
            Thread(target=worker.start, daemon=True).start()
            logging.info("Started Celery")



    # Register blueprints
    from .routes.main import main as main_blueprint
    from .routes.api import api as api_blueprint
    if 'main' not in app.blueprints:
        app.register_blueprint(main_blueprint, name='main')
    if 'api' not in app.blueprints:
        app.register_blueprint(api_blueprint, url_prefix='/api', name='api')

    # Setup database
    with app.app_context():
        db.create_all()
        # Create file watcher
        from app.tasks.file_watcher import setup_file_watcher
        setup_file_watcher(app)

    return app
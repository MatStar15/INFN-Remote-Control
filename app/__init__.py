from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from kombu import Connection
from celery import Celery
import os

import logging

def get_socketio():
    return SocketIO(message_queue=os.environ.get('SOCKETIO_MESSAGE_QUEUE', 'redis://'),)

# Initialize extensions
db = SQLAlchemy()

socketio = SocketIO()


@socketio.on('error')
def handle_error(e):
    print(f"Socket error: {e}")
    return {'message': 'Error handling socket event'}


def emit_job_update(job):
    external_socketio = get_socketio()
    external_socketio.emit('job_update', {'job': job.to_dict()})
    print(f"Emitted job update for job {job.id} to all clients")


def emit_new_file(file, job_id):
    external_socketio = get_socketio()
    external_socketio.emit('new_file',
                 {'file': file.to_dict(), 'job_id': job_id})
    print(f"Emitted new file for job {job_id} to all clients")

def emit_file_analyzed(file, job_id):
    external_socketio = get_socketio()
    external_socketio.emit('file_analyzed',
                 {'file': file.to_dict(), 'job_id': job_id})
    print(f"Emitted file analyzed for job {job_id} to all clients")


@socketio.on('connect')
def handle_connect():
    print("Socket connected")
    socketio.emit('welcome', {'message': 'Hi! Welcome to the server'})
    return {'message': 'Connected to socket'}

@socketio.on('test')
def handle_connect():
    print("test received from client")
    socketio.emit('test', {'message': 'TEST'})


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

    # Set up logging
    # logging.basicConfig(level=logging.INFO)
    # app.logger.setLevel(logging.INFO)

    return app
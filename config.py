import os

"""
1. Start Redis from Docker (or locally)
2. Start the Flask application
"""

# noinspection GrazieInspection
class Config:
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME', '127.0.0.1')  # change this to host.docker.internal if needed

    # File watcher configuration
    RESULT_FILE_EXTENSION = os.environ.get('RESULT_FILE_EXTENSION',
                                           r'.raw')  # Change this to your desired pattern for raw files
    ANALYZED_FILE_EXTENSION = os.environ.get('ANALYZED_FILE_EXTENSION',
                                             r'.analyzed')  # Change this to your desired pattern for analyzed files

    RESULTS_DIRECTORY = os.environ.get(
        'RESULTS_DIRECTORY',  # TODO: show in the
        '/mnt/c/users/user/PycharmProjects/INFN-test/results'  # Change this to your desired directory
    )

    AUTO_ANALYZE_FILES = os.environ.get(
        'AUTO_ANALYZE_FILES',
        'False'  # Change this to True if you want to auto-analyze files
    ).lower() == 'True'


    # Celery configuration
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'UTC'
    enable_utc = True
    broker_connection_retry_on_startup = True
    include = ['celery_worker', 'app']
    tasks = ['celery_worker.run_calculation', 'celery_worker.analyze_file']
    hostname = 'celery@localhost'
    worker_pool = 'solo'
    broker_url = f'redis://{REDIS_HOSTNAME}:6379/0'
    result_backend = f'redis://{REDIS_HOSTNAME}:6379/0'
    broker_transport = 'redis'

    # SocketIO configuration
    SOCKETIO_MESSAGE_QUEUE = 'redis://'


# DB Configuration for different environments
class DevelopmentConfig(Config):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///dev.db')

class ProductionConfig(Config):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod.db')

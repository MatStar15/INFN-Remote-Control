import os

"""
1. Start Redis from Docker, can be done using services in pycharm
2. Start the Celery worker using the following command:
    celery -A celery_worker.celery -b redis://host.docker.internal:6379/0 worker  --loglevel=info -E --pool=solo
    or
    celery -A celery_worker.celery -b redis://127.0.0.1:6379/0 worker --loglevel=info -E --pool=solo
    
    (ADD LAST PART ONLY IF YOU ARE USING WINDOWS, single worker thread)
    
3. Start the Flask application 
"""

# noinspection GrazieInspection
class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME', '127.0.0.1')

    # Use full Redis URL with host.docker.internal for Windows
    CELERY_BROKER_URL = os.environ.get(
        'broker_url',
        f'redis://{REDIS_HOSTNAME}:6379/0'
    )
    CELERY_RESULT_BACKEND = os.environ.get(
        'result_backend',
        f'redis://{REDIS_HOSTNAME}:6379/0'
    )

    BROKER_TRANSPORT = 'redis'

    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

    # File watcher configuration
    RESULT_FILE_PATTERN = os.environ.get('RESULT_FILE_PATTERN', r'.*\.raw$')
    ANALYZED_FILE_PATTERN = os.environ.get('ANALYZED_FILE_PATTERN', r'.*\.analyzed$')

    RESULTS_DIRECTORY = os.environ.get(
        'RESULTS_DIRECTORY',
        'C:\\Users\\user\\PycharmProjects\\INFN-test\\results'
    )
    AUTO_ANALYZE_FILES = os.environ.get(
        'AUTO_ANALYZE_FILES',
        'False'
    ).lower() == 'true'

    # Celery configuration
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'UTC'
    CELERY_ENABLE_UTC = True
    broker_connection_retry_on_startup = True

    # File Extensions:
    RAW_FILE_EXTENSION = r'\.raw$'
    ANALYZED_FILE_EXTENSION = r'\.analyzed$'

    # FLASK_DEBUG = True

    SOCKETIO_MESSAGE_QUEUE = 'redis://'

class DevelopmentConfig(Config):
    """Development configuration"""
    # FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///dev.db')

class ProductionConfig(Config):
    """Production configuration"""
    # FLASK_DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod.db')

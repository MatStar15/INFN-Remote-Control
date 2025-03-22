from app import create_app, celery
import os, logging

# Import tasks here to register them
from app.tasks.calculation import run_calculation
from app.tasks.analysis import analyze_file

# Debug prints
logging.info("CELERY_BROKER_URL:", os.environ.get('broker_url'))
logging.info("REDIS Hostname:", os.environ.get('REDIS_HOSTNAME', 'host.docker.internal'))
logging.info("REDIS URL:", f'redis://{os.environ.get("REDIS_HOSTNAME", "host.docker.internal")}:6379/0')


app = create_app()
app.app_context().push()

celery.conf.update(app.config)


from app import create_app, celery
import os

# Import tasks here to register them
from app.tasks.calculation import run_calculation
from app.tasks.analysis import analyze_file

# Debug prints
print("CELERY_BROKER_URL:", os.environ.get('CELERY_BROKER_URL'))
print("REDIS Hostname:", os.environ.get('REDIS_HOSTNAME', 'host.docker.internal'))

app = create_app()
app.app_context().push()

celery.conf.update(app.config)


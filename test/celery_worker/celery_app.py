from celery import Celery
import time

app = Celery('hello_world',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

@app.task
def hello_world():
    time.sleep(2)  # Simulate some work
    message = "Hello, World!"
    print(message)  # This will show in worker logs
    return message
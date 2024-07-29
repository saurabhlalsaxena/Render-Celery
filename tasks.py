from celery import Celery
import os
import time

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')

celery = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)

@celery.task(name='tasks.long_running_task')
def long_running_task(seconds):
    time.sleep(seconds)
    return f"Task completed after {seconds} seconds"
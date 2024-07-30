from celery import Celery
import os
import time

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')

celery = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)
celery.conf.broker_connection_retry_on_startup = True

# Flower configuration
celery.conf.update(
    broker_url=REDIS_URL,
    result_backend=REDIS_URL,
    flower_port=5555,
)

@celery.task(name='tasks.long_running_task')
def long_running_task(seconds):
    time.sleep(seconds)
    return f'Task completed after {seconds} seconds'
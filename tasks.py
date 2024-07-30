from celery import Celery
import os
import time
from kombu.connection import Connection

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')

# Connection pool settings
pool_limit = 100  # Adjust this value based on your needs

celery = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)
celery.conf.broker_connection_retry_on_startup = True

# Connection pool configuration
celery.conf.broker_pool_limit = pool_limit
celery.conf.redis_max_connections = pool_limit

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

# Create a connection pool
connection_pool = Connection(REDIS_URL).Pool(limit=pool_limit)
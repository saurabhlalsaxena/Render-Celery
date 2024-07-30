from celery import Celery
import os
import time
from kombu import Connection
from kombu.utils.functional import retry_over_time
from redis.exceptions import ConnectionError

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')

# Set a very conservative pool limit
pool_limit = 5

def get_redis_connection():
    return retry_over_time(
        Connection(REDIS_URL).connect,
        retry_on_exception=lambda exc: isinstance(exc, ConnectionError),
        max_retries=3,
        interval_start=1,
        interval_step=1,
        interval_max=3,
    )

celery = Celery('tasks')
celery.conf.update(
    broker_url=REDIS_URL,
    result_backend=REDIS_URL,
    broker_pool_limit=pool_limit,
    redis_max_connections=pool_limit,
    broker_connection_retry_on_startup=True,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=10,
    worker_concurrency=pool_limit,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_default_rate_limit='10/m',
    flower_port=5555,
)

@celery.task(name='tasks.long_running_task', bind=True, max_retries=3)
def long_running_task(self, seconds):
    try:
        time.sleep(seconds)
        return f'Task completed after {seconds} seconds'
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

# Create a connection pool
connection_pool = Connection(REDIS_URL).Pool(limit=pool_limit)
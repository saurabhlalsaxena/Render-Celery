from celery import Celery
import os
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')

celery = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)
celery.conf.broker_connection_retry_on_startup = True

@celery.task(name='tasks.long_running_task')
def long_running_task(seconds):
    time.sleep(seconds)
    return f'Task completed after {seconds} seconds'

# Simple HTTP server
class SimpleServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Celery worker is running')

def run_http_server():
    port = int(os.environ.get('PORT', 8080))
    httpd = HTTPServer(('0.0.0.0', port), SimpleServer)
    httpd.serve_forever()

# Start HTTP server in a separate thread
threading.Thread(target=run_http_server, daemon=True).start()
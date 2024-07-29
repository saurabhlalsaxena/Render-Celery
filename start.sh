#!/bin/bash

# Start the HTTP server
python -m http.server $PORT &

# Start the Celery worker
celery -A tasks worker --loglevel=info
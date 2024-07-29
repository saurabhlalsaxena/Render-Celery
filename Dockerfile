# Use a more recent and slim Python image
FROM python:3.11-slim-bullseye

# Install Poetry
RUN pip install poetry==1.6.1

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Set the working directory
WORKDIR /code

# Copy only the necessary files for Poetry to install dependencies
COPY ./pyproject.toml ./poetry.lock* ./

# Install dependencies without creating a virtual environment
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY tasks.py ./

RUN poetry install --no-interaction --no-ansi

# Install Celery
RUN pip install --no-cache-dir celery[redis]

# Set environment variable for Redis URL (can be overridden at runtime)
#ENV REDIS_URL=redis://redis:6379/0

# Start the Celery worker
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
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

# Copy the tasks.py file
COPY tasks.py ./

RUN poetry install --no-interaction --no-ansi

# Install Celery
RUN pip install --no-cache-dir celery[redis]

# Create a non-root user
RUN useradd -m celery-user

# Change ownership of the working directory
RUN chown -R celery-user:celery-user /code

# Switch to the non-root user
USER celery-user

# Expose the port the app runs on
EXPOSE 8080

# Start the Celery worker and Python script
CMD celery -A tasks worker --loglevel=info & python tasks.py
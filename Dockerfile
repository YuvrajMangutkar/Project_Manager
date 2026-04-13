# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (e.g., for PlantUML or other diagram generators if needed)
RUN apt-get update && apt-get install -y \
    graphviz \
    default-jre \
    wget \
    curl \
    && wget -O /app/plantuml.jar https://github.com/plantuml/plantuml/releases/download/v1.2023.13/plantuml-1.2023.13.jar \
    && rm -rf /var/lib/apt/lists/*

# NOTE: Ollama local installation may fail in Render environment; use external Ollama host (OLLAMA_HOST) or OpenAI fallback.

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN cd frontend && python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn or django development server
WORKDIR /app/frontend
CMD sh -c "python manage.py migrate && gunicorn --bind 0.0.0.0:${PORT:-8000} core.wsgi:application"

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Diagrams use the free PlantUML public server — no Java or plantuml.jar needed
# Only curl is kept for basic health-check ability
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

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

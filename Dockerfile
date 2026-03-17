# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (e.g., for PlantUML or other diagram generators if needed)
RUN apt-get update && apt-get install -y \
    graphviz \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run gunicorn or django development server
WORKDIR /app/frontend
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]

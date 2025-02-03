# Use the official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to optimize caching
COPY requirements.txt /app/requirements.txt

# Install dependencies first (before copying full project)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project after installing dependencies
COPY . /app/

# Expose port 8000 for the Django app
EXPOSE 8000

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "faq_system.wsgi:application"]
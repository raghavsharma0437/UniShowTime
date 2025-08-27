# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        libxml2-dev \
        libxslt-dev \
        libssl-dev \
        libffi-dev \
        libjpeg-dev \
        libpng-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional production dependencies
RUN pip install --no-cache-dir \
    psycopg2-binary==2.9.7 \
    dj-database-url==2.1.0 \
    python-decouple==3.8

# Copy project
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

# Don't switch to appuser yet - run setup as root first
# Collect static files as root
RUN python manage.py collectstatic --noinput --clear || echo "Static files collection failed, continuing..."

# Now switch to appuser
USER appuser

# Expose port
EXPOSE 8000

# Use a simpler command that doesn't rely on shell script
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "--log-level", "info", "UniShowTime.wsgi:application"]

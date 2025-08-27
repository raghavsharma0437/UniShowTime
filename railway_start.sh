#!/bin/bash

# Simple Railway startup script

echo "🚀 Starting Railway deployment..."

# Set default port if not provided
export PORT=${PORT:-8000}

# Run migrations (this should happen automatically in Railway)
echo "📊 Running database migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

echo "🎯 Starting Gunicorn server on port $PORT..."

# Start Gunicorn with Railway-compatible settings
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    UniShowTime.wsgi:application

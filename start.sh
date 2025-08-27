#!/bin/bash

# Railway deployment script for UniShowTime

echo "Starting Railway deployment setup..."

# Wait for database to be available
echo "Checking database connection..."
python manage.py check --database default

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (optional)
echo "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created with username: admin, password: admin123')
else:
    print('Superuser already exists.')
"

echo "Setup complete. Starting Gunicorn server..."

# Start Gunicorn with proper port handling
PORT=${PORT:-8000}
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 --timeout 120 --log-level info UniShowTime.wsgi:application

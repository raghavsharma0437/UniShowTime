#!/bin/bash

# Railway deployment script for UniShowTime

echo "Starting Railway deployment setup..."

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
    print('No superuser found. Create one manually after deployment.')
else:
    print('Superuser already exists.')
"

echo "Setup complete. Starting Gunicorn server..."

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 UniShowTime.wsgi:application

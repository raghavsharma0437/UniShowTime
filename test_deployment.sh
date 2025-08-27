#!/bin/bash

echo "🧪 Testing Railway deployment locally..."

# Set test environment variables
export RAILWAY_ENVIRONMENT=production
export SECRET_KEY=test-secret-key-for-local-testing
export DEBUG=False

echo "📊 Running Django check..."
python manage.py check

echo "🗄️ Testing database connection..."
python manage.py check --database default

echo "📁 Testing static files collection..."
python manage.py collectstatic --noinput --dry-run

echo "🌐 Testing health endpoint..."
python manage.py shell -c "
from django.test import Client
client = Client()
response = client.get('/health/')
print(f'Health check status: {response.status_code}')
print(f'Health check content: {response.content.decode()}')
"

echo "✅ Local tests completed!"

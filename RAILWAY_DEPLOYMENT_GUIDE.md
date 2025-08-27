# 🚀 UniShowTime - Railway Deployment Guide with Docker

This comprehensive guide will help you deploy the UniShowTime Django project on Railway using Docker.

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Project Preparation](#project-preparation)
4. [Docker Configuration](#docker-configuration)
5. [Railway Setup](#railway-setup)
6. [Environment Variables](#environment-variables)
7. [Database Configuration](#database-configuration)
8. [Deployment Steps](#deployment-steps)
9. [Post-Deployment Setup](#post-deployment-setup)
10. [Troubleshooting](#troubleshooting)

## 📊 Project Overview

**UniShowTime** is a Django-based university event management platform with:
- **Backend**: Django 5.1+ (Python)
- **Database**: SQLite (dev) → PostgreSQL (production)
- **Frontend**: Django Templates + TailwindCSS
- **Features**: Event management, QR code tickets, user roles, event suggestions

## ✅ Prerequisites

Before starting, ensure you have:
- [ ] **Git** installed
- [ ] **Python 3.11+** installed
- [ ] **Docker Desktop** installed and running
- [ ] **Railway account** (sign up at [railway.app](https://railway.app))
- [ ] **GitHub account** (for code repository)

## 🛠️ Project Preparation

### 1. Clone and Prepare the Project

```bash
# Clone the project
git clone <your-repo-url>
cd UniShowTime-main

# Create a new Git repository (if not already initialized)
git init
git add .
git commit -m "Initial commit"

# Push to your GitHub repository
git remote add origin https://github.com/yourusername/UniShowTime.git
git push -u origin main
```

### 2. Update Project Structure

The current project needs some modifications for production deployment:

```
UniShowTime/
├── Dockerfile              # ← We'll create this
├── docker-compose.yml      # ← We'll create this
├── .env.example           # ← We'll create this
├── railway.toml           # ← We'll create this
├── requirements.txt       # ← Already exists
├── manage.py             # ← Already exists
├── UniShowTime/          # ← Main Django project
│   ├── settings.py       # ← We'll modify this
│   ├── wsgi.py          # ← Already exists
│   └── ...
└── mainapp/             # ← Main Django app
    └── ...
```

## 🐳 Docker Configuration

### 1. Create Dockerfile

Create `Dockerfile` in the root directory:

```dockerfile
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

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "UniShowTime.wsgi:application"]
```

### 2. Create .dockerignore

Create `.dockerignore` file:

```
__pycache__
*.pyc
*.pyo
*.pyd
.git
.gitignore
README.md
.env
.venv
venv/
UniShowTimeenv/
.DS_Store
*.sqlite3
media/backups/
node_modules/
.pytest_cache
.coverage
htmlcov/
```

### 3. Create docker-compose.yml (for local testing)

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DATABASE_URL=sqlite:///db.sqlite3
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: unishowtime
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - "5432:5432"

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## ⚙️ Update Django Settings

### 1. Create Production Settings

Create a new file `UniShowTime/production_settings.py`:

```python
from .settings import *
import os
import dj_database_url
from decouple import config

# Security Settings
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')

# Allowed Hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',
    config('RAILWAY_STATIC_URL', default=''),
    config('RAILWAY_PUBLIC_DOMAIN', default=''),
]

# Remove localhost and 127.0.0.1 from ALLOWED_HOSTS for production
if not DEBUG:
    ALLOWED_HOSTS = [host for host in ALLOWED_HOSTS if host not in ['localhost', '127.0.0.1']]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3')
    )
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 86400
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# WhiteNoise configuration
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email configuration (update with your SMTP settings)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### 2. Update requirements.txt

Add these dependencies to `requirements.txt`:

```
Django>=4.2.0
Pillow>=10.0.0
qrcode>=7.4.2
python-dotenv>=1.0.0
django-tailwind>=3.6.0
django-browser-reload>=1.12.0
django-crispy-forms>=2.0
crispy-tailwind>=0.5.0
whitenoise>=6.0.0
gunicorn>=21.0.0
django-compressor>=4.0
django-libsass>=0.9
django-debug-toolbar>=4.0.0
# Production dependencies
psycopg2-binary==2.9.7
dj-database-url==2.1.0
python-decouple==3.8
```

### 3. Create .env.example

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Railway Configuration
RAILWAY_STATIC_URL=
RAILWAY_PUBLIC_DOMAIN=
SECURE_SSL_REDIRECT=True
```

## 🚆 Railway Setup

### 1. Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your UniShowTime repository

### 2. Create railway.toml

Create `railway.toml` in your project root:

```toml
[build]
builder = "dockerfile"

[deploy]
healthcheckPath = "/"
healthcheckTimeout = 100
restartPolicyType = "never"
```

### 3. Add PostgreSQL Database

1. In Railway dashboard, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a PostgreSQL database
4. Note the database connection details

## 🔧 Environment Variables

In Railway dashboard, go to your project → Variables, and add:

```
SECRET_KEY=your-generated-secret-key
DEBUG=False
DATABASE_URL=postgresql://postgres:password@host:5432/railway
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
RAILWAY_STATIC_URL=${{RAILWAY_STATIC_URL}}
RAILWAY_PUBLIC_DOMAIN=${{RAILWAY_PUBLIC_DOMAIN}}
```

### Generate SECRET_KEY

```python
# Run this in Python shell to generate a secret key
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## 📊 Database Configuration

### 1. Update Django Settings

Modify `UniShowTime/settings.py` to detect environment:

```python
import os

# Detect if we're on Railway
if 'RAILWAY_ENVIRONMENT' in os.environ:
    from .production_settings import *
```

### 2. Database Migration Strategy

Your app will need to run migrations on first deployment:

```bash
# Railway will automatically run these during deployment
python manage.py migrate
python manage.py collectstatic --noinput
```

## 🚀 Deployment Steps

### 1. Final Code Preparation

```bash
# Make sure all files are added
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 2. Deploy on Railway

1. **Connect Repository**: Railway should automatically detect your repository
2. **Set Environment Variables**: Add all variables mentioned above
3. **Deploy**: Railway will automatically build and deploy your Docker container

### 3. Monitor Deployment

1. Check Railway logs for any errors
2. Verify the app is running at your Railway URL
3. Check database connectivity

## 🔧 Post-Deployment Setup

### 1. Create Superuser

```bash
# Access Railway shell
railway shell

# Create superuser
python manage.py createsuperuser
```

### 2. Initial Data Setup

```bash
# Load any initial data (if you have fixtures)
python manage.py loaddata your_fixture.json

# Or create departments manually through Django admin
```

### 3. Test Core Features

- [ ] User registration/login
- [ ] Event creation
- [ ] Ticket booking
- [ ] QR code generation
- [ ] Admin panel access
- [ ] Media file uploads

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Static Files Not Loading
```bash
# Ensure WhiteNoise is properly configured
# Check STATIC_ROOT and STATIC_URL settings
# Verify collectstatic runs successfully
```

#### 2. Database Connection Issues
```bash
# Verify DATABASE_URL format
# Check PostgreSQL service is running
# Ensure migrations are applied
```

#### 3. Media Files Not Uploading
```bash
# For Railway, consider using external storage like AWS S3
# Or check MEDIA_ROOT permissions
```

#### 4. Environment Variables Not Loading
```bash
# Verify variables are set in Railway dashboard
# Check variable names (case-sensitive)
# Restart the deployment
```

### 5. Railway-Specific Commands

```bash
# View logs
railway logs

# Access shell
railway shell

# Restart service
railway redeploy
```

## 📝 Additional Considerations

### 1. File Storage for Production

For production, consider using cloud storage:

```python
# Add to production_settings.py for file storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='')
```

### 2. Custom Domain Setup

1. In Railway dashboard → Settings → Domains
2. Add your custom domain
3. Update ALLOWED_HOSTS in settings

### 3. SSL Certificate

Railway automatically provides SSL certificates for Railway domains.

## 🎯 Final Checklist

- [ ] Dockerfile created and tested
- [ ] Production settings configured
- [ ] Environment variables set in Railway
- [ ] PostgreSQL database connected
- [ ] Static files configuration working
- [ ] Media files handling configured
- [ ] Superuser created
- [ ] Core functionality tested
- [ ] Error monitoring setup
- [ ] Backup strategy planned

## 🔗 Useful Links

- [Railway Documentation](https://docs.railway.app)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)

---

🎉 **Congratulations!** Your UniShowTime project should now be successfully deployed on Railway with Docker!

For support or issues, refer to the troubleshooting section or check Railway's documentation.

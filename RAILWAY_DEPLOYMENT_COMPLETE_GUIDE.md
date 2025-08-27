# 🚀 Complete Railway Deployment Guide for UniShowTime Django Project

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [GitHub Repository Setup](#github-repository-setup)
4. [Railway Project Setup](#railway-project-setup)
5. [Environment Variables Configuration](#environment-variables-configuration)
6. [Database Setup](#database-setup)
7. [Deployment Process](#deployment-process)
8. [Post-Deployment Tasks](#post-deployment-tasks)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance & Updates](#maintenance--updates)

---

## 📊 Project Overview

**UniShowTime** is a Django-based university event management platform featuring:
- **Backend**: Django 5.1+ with Python 3.11
- **Database**: PostgreSQL (Railway managed)
- **Frontend**: Django Templates with TailwindCSS
- **Features**: Event management, QR tickets, user authentication, admin dashboard

---

## ✅ Prerequisites

Before starting deployment, ensure you have:
- [x] **GitHub account** with your project repository
- [x] **Railway account** (sign up at [railway.app](https://railway.app))
- [x] **Gmail account** (for email functionality)
- [x] **Project files** properly configured

---

## 🔧 GitHub Repository Setup

### 1. Repository Structure
Your project should have this structure:
```
UniShowTime/
├── Dockerfile                 # Docker configuration
├── railway.toml              # Railway configuration
├── requirements.txt          # Python dependencies
├── manage.py                # Django management script
├── UniShowTime/             # Main Django project
│   ├── settings.py          # Base settings
│   ├── production_settings.py # Production settings
│   ├── urls.py              # URL configuration
│   └── wsgi.py              # WSGI application
├── mainapp/                 # Main Django app
└── templates/               # HTML templates
```

### 2. Required Files

**Dockerfile:**
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

# Create staticfiles and media directories with proper permissions
RUN mkdir -p /app/staticfiles /app/media && \
    chmod -R 755 /app/staticfiles /app/media

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

# Switch to appuser
USER appuser

# Expose port
EXPOSE 8000

# Startup command with verbose logging
CMD ["sh", "-c", "echo 'Starting Railway deployment...' && python manage.py check && echo 'Django check passed' && python manage.py migrate --noinput && echo 'Migrations completed' && python manage.py collectstatic --noinput --clear && echo 'Static files collected' && echo 'Starting Gunicorn...' && gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120 --log-level info --access-logfile - --error-logfile - UniShowTime.wsgi:application"]
```

**railway.toml:**
```toml
[build]
builder = "dockerfile"

[deploy]
healthcheckPath = "/health/"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
```

**requirements.txt:**
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

---

## 🚆 Railway Project Setup

### 1. Create Railway Project

1. **Login to Railway**: Go to [railway.app](https://railway.app)
2. **New Project**: Click "New Project"
3. **Deploy from GitHub**: Select "Deploy from GitHub repo"
4. **Connect Repository**: Choose your `UniShowTime` repository
5. **Configure Service**: Railway will detect your Dockerfile automatically

### 2. Add PostgreSQL Database

1. **Add Service**: In your Railway project, click "New Service"
2. **Add Database**: Select "Database" → "PostgreSQL"
3. **Database Creation**: Railway automatically creates a PostgreSQL instance
4. **Note Credentials**: Save the database connection details

---

## 🔧 Environment Variables Configuration

### 1. PostgreSQL Database Variables (Auto-Generated)

Railway automatically creates these for your PostgreSQL service:
```env
DATABASE_PUBLIC_URL="postgresql://${{PGUSER}}:${{POSTGRES_PASSWORD}}@${{RAILWAY_TCP_PROXY_DOMAIN}}:${{RAILWAY_TCP_PROXY_PORT}}/${{PGDATABASE}}"
DATABASE_URL="postgresql://${{PGUSER}}:${{POSTGRES_PASSWORD}}@${{RAILWAY_PRIVATE_DOMAIN}}:5432/${{PGDATABASE}}"
PGDATA="/var/lib/postgresql/data/pgdata"
PGDATABASE="${{POSTGRES_DB}}"
PGHOST="${{RAILWAY_PRIVATE_DOMAIN}}"
PGPASSWORD="${{POSTGRES_PASSWORD}}"
PGPORT="5432"
PGUSER="${{POSTGRES_USER}}"
POSTGRES_DB="railway"
POSTGRES_PASSWORD="jTLUNqeBFSbnYnOhelOpNonEHHzKGFBe"
POSTGRES_USER="postgres"
RAILWAY_DEPLOYMENT_DRAINING_SECONDS="60"
SSL_CERT_DAYS="820"
```

### 2. Django Application Variables (Manual Setup Required)

Go to **Railway Dashboard → Your Project → Variables** and add these:

#### Core Django Settings:
```env
SECRET_KEY="AxJ_r2RWvkwvXe9o_z2=PUxVXPlZ=M-yM4B515ktQ=naqVQGtD"
DEBUG="False"
RAILWAY_ENVIRONMENT="production"
```

#### Database Configuration:
```env
DATABASE_URL="postgresql://postgres:jTLUNqeBFSbnYnOhelOpNonEHHzKGFBe@${{RAILWAY_PRIVATE_DOMAIN}}:5432/railway"
```

#### Email Configuration:
```env
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT="587"
EMAIL_USE_TLS="True"
EMAIL_HOST_USER="meetdoshi2109@gmail.com"
EMAIL_HOST_PASSWORD="dqgz myhb iskt cdzf"
```

#### Security Settings:
```env
SECURE_SSL_REDIRECT="True"
```

#### Railway Built-in Variables:
```env
RAILWAY_STATIC_URL="${{RAILWAY_STATIC_URL}}"
RAILWAY_PUBLIC_DOMAIN="${{RAILWAY_PUBLIC_DOMAIN}}"
```

### 3. How to Generate SECRET_KEY

Run this command locally to generate a new SECRET_KEY:
```bash
python3 -c "import secrets; import string; chars = string.ascii_letters + string.digits + '_-+='; print(''.join(secrets.choice(chars) for i in range(50)))"
```

### 4. Gmail App Password Setup

For email functionality:
1. **Enable 2FA**: Go to Google Account → Security → 2-Step Verification
2. **Generate App Password**: Security → App passwords → Select app → Generate
3. **Use App Password**: Use the 16-character password in `EMAIL_HOST_PASSWORD`

---

## 🗄️ Database Setup

### 1. Database Connection String Format

The `DATABASE_URL` follows this format:
```
postgresql://username:password@host:port/database_name
```

For your setup:
```
postgresql://postgres:jTLUNqeBFSbnYnOhelOpNonEHHzKGFBe@${{RAILWAY_PRIVATE_DOMAIN}}:5432/railway
```

### 2. Database Configuration in Django

**UniShowTime/production_settings.py:**
```python
from .settings import *
import os
import dj_database_url
from pathlib import Path

# Ensure BASE_DIR is properly set
BASE_DIR = Path(__file__).resolve().parent.parent

# Debug prints to see what's happening
print("🔧 Production settings loading...")
print(f"📂 BASE_DIR: {BASE_DIR}")
print(f"🔑 SECRET_KEY set: {'Yes' if os.environ.get('SECRET_KEY') else 'No'}")
print(f"🗄️ DATABASE_URL set: {'Yes' if os.environ.get('DATABASE_URL') else 'No'}")

# Override settings for production
DEBUG = False

# Simple secret key handling
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-in-production')

# Allow all hosts for Railway
ALLOWED_HOSTS = ['*']

# Database configuration using Railway's DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"🗄️ Database URL: {DATABASE_URL[:50] if DATABASE_URL else 'Not set'}...")

if DATABASE_URL:
    try:
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL)
        }
        print("✅ Database configuration successful")
    except Exception as e:
        print(f"❌ Database configuration failed: {e}")
        # Fallback to SQLite
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
        print("🔄 Using SQLite fallback")
else:
    # Fallback to SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("⚠️ No DATABASE_URL found, using SQLite")

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles'  # Use absolute path for Railway

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'  # Use absolute path for Railway

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 86400
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# WhiteNoise configuration - use simpler storage for Railway
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'  # Simpler storage
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### 3. Environment Detection in Base Settings

**UniShowTime/settings.py** (add this at the top):
```python
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Detect if we're on Railway or in production
if 'RAILWAY_ENVIRONMENT' in os.environ:
    print("🚀 Running in Railway environment - using production settings")
    # Import production settings
    try:
        from .production_settings import *
    except ImportError as e:
        print(f"⚠️ Failed to import production settings: {e}")
        pass
else:
    print("💻 Running in development environment")
    # Development settings continue below
    pass
```

---

## 🚀 Deployment Process

### 1. Pre-Deployment Checklist

- [x] GitHub repository is up to date
- [x] All required files are present (Dockerfile, railway.toml, requirements.txt)
- [x] Production settings are configured
- [x] Environment variables are set in Railway

### 2. Deploy to Railway

1. **Push to GitHub**: Ensure all changes are committed and pushed
   ```bash
   git add .
   git commit -m "Railway deployment configuration"
   git push origin main
   ```

2. **Automatic Deployment**: Railway automatically detects the push and starts deployment

3. **Monitor Build Logs**: Watch the build process in Railway dashboard

4. **Monitor Application Logs**: Check the application startup logs for any errors

### 3. Build Process

Railway will execute these steps:
1. **Docker Build**: Build the Docker image using your Dockerfile
2. **Dependencies Installation**: Install Python packages from requirements.txt
3. **Image Creation**: Create the final Docker image
4. **Container Startup**: Start the container with your CMD command

### 4. Health Check

Railway performs health checks on `/health/` endpoint:
- **Timeout**: 5 minutes
- **Expected Response**: HTTP 200 with "OK" content
- **Retry Policy**: Continues retrying until timeout

---

## 🔧 Post-Deployment Tasks

### 1. Create Superuser

Access Railway shell and create an admin user:
```bash
# In Railway dashboard → Your service → Shell
python manage.py createsuperuser
```

Or use the automatic superuser creation (already configured):
- **Username**: admin
- **Password**: admin123
- **Email**: admin@example.com

### 2. Verify Functionality

Test these features:
- [x] **Admin Panel**: Access `/django-admin/`
- [x] **User Registration**: Test user signup
- [x] **Event Creation**: Create sample events
- [x] **Database**: Verify data persistence
- [x] **Static Files**: Check CSS/JS loading
- [x] **Media Files**: Test image uploads

### 3. Custom Domain (Optional)

1. **Add Domain**: Railway Dashboard → Settings → Domains
2. **DNS Configuration**: Point your domain to Railway
3. **SSL Certificate**: Railway automatically provides SSL
4. **Update Settings**: Add domain to `ALLOWED_HOSTS`

---

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Health Check Failures
**Symptoms**: "service unavailable" during health check
**Solutions**:
- Check application logs for startup errors
- Verify environment variables are set correctly
- Ensure database connection is working
- Check if the health endpoint is accessible

#### 2. Static Files Not Loading
**Symptoms**: Missing CSS/JS on the website
**Solutions**:
- Verify `STATIC_ROOT` is set to `/app/staticfiles`
- Check WhiteNoise middleware is installed
- Run `python manage.py collectstatic` manually

#### 3. Database Connection Errors
**Symptoms**: "database connection failed" errors
**Solutions**:
- Verify `DATABASE_URL` format is correct
- Check PostgreSQL service is running
- Ensure database credentials are correct

#### 4. Import Errors
**Symptoms**: "ModuleNotFoundError" during startup
**Solutions**:
- Check all dependencies are in `requirements.txt`
- Verify Python version compatibility
- Check for missing system packages in Dockerfile

#### 5. Environment Variables Not Loading
**Symptoms**: Settings not applying correctly
**Solutions**:
- Verify variables are set in Railway dashboard
- Check variable names are exact (case-sensitive)
- Restart the deployment

### Debug Commands

Access Railway shell for debugging:
```bash
# Check Django configuration
python manage.py check

# Test database connection
python manage.py check --database default

# Check environment variables
python manage.py shell -c "import os; print('SECRET_KEY:', bool(os.environ.get('SECRET_KEY')))"

# Test static files
python manage.py collectstatic --dry-run

# Check health endpoint
curl http://localhost:8000/health/
```

---

## 🔄 Maintenance & Updates

### 1. Code Updates

For code changes:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```
Railway automatically redeploys on push.

### 2. Environment Variable Updates

1. **Railway Dashboard**: Go to Variables section
2. **Modify Variables**: Update existing or add new variables
3. **Restart Service**: Railway automatically restarts the service

### 3. Database Migrations

For database schema changes:
```bash
# Migrations run automatically during deployment
# Or manually in Railway shell:
python manage.py makemigrations
python manage.py migrate
```

### 4. Backup Strategy

- **Database Backups**: Railway provides automatic PostgreSQL backups
- **Media Files**: Consider using external storage (AWS S3, Cloudinary)
- **Code Backup**: GitHub repository serves as code backup

---

## 📞 Support Resources

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Django Deployment Guide**: [docs.djangoproject.com](https://docs.djangoproject.com/en/stable/howto/deployment/)
- **PostgreSQL Documentation**: [postgresql.org/docs](https://www.postgresql.org/docs/)

---

## 🎯 Complete Environment Variables Checklist

### ✅ Required Variables (Set in Railway Dashboard):

```env
# Core Django Settings
SECRET_KEY="AxJ_r2RWvkwvXe9o_z2=PUxVXPlZ=M-yM4B515ktQ=naqVQGtD"
DEBUG="False"
RAILWAY_ENVIRONMENT="production"

# Database Configuration
DATABASE_URL="postgresql://postgres:jTLUNqeBFSbnYnOhelOpNonEHHzKGFBe@${{RAILWAY_PRIVATE_DOMAIN}}:5432/railway"

# Email Configuration
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT="587"
EMAIL_USE_TLS="True"
EMAIL_HOST_USER="meetdoshi2109@gmail.com"
EMAIL_HOST_PASSWORD="dqgz myhb iskt cdzf"

# Security Settings
SECURE_SSL_REDIRECT="True"

# Railway Built-in Variables
RAILWAY_STATIC_URL="${{RAILWAY_STATIC_URL}}"
RAILWAY_PUBLIC_DOMAIN="${{RAILWAY_PUBLIC_DOMAIN}}"
```

### ⚡ Automatic Variables (Generated by Railway PostgreSQL):

```env
DATABASE_PUBLIC_URL="postgresql://${{PGUSER}}:${{POSTGRES_PASSWORD}}@${{RAILWAY_TCP_PROXY_DOMAIN}}:${{RAILWAY_TCP_PROXY_PORT}}/${{PGDATABASE}}"
DATABASE_URL="postgresql://${{PGUSER}}:${{POSTGRES_PASSWORD}}@${{RAILWAY_PRIVATE_DOMAIN}}:5432/${{PGDATABASE}}"
PGDATA="/var/lib/postgresql/data/pgdata"
PGDATABASE="${{POSTGRES_DB}}"
PGHOST="${{RAILWAY_PRIVATE_DOMAIN}}"
PGPASSWORD="${{POSTGRES_PASSWORD}}"
PGPORT="5432"
PGUSER="${{POSTGRES_USER}}"
POSTGRES_DB="railway"
POSTGRES_PASSWORD="jTLUNqeBFSbnYnOhelOpNonEHHzKGFBe"
POSTGRES_USER="postgres"
RAILWAY_DEPLOYMENT_DRAINING_SECONDS="60"
SSL_CERT_DAYS="820"
```

---

🎉 **Congratulations!** Your UniShowTime Django project is now fully deployed on Railway with PostgreSQL database and proper environment configuration!

For any issues or questions, refer to the troubleshooting section or check the Railway dashboard logs for detailed error information.

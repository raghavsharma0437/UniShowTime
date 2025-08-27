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

# Debug: List all environment variables that might contain database info
print("🔍 Available database-related environment variables:")
for key, value in os.environ.items():
    if any(keyword in key.upper() for keyword in ['DATABASE', 'POSTGRES', 'DB', 'PG']):
        print(f"   {key}: {value[:50] if len(value) > 50 else value}...")
        
print("🔍 Available Railway-related environment variables:")
for key, value in os.environ.items():
    if 'RAILWAY' in key.upper():
        print(f"   {key}: {value[:50] if len(value) > 50 else value}...")

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

# WhiteNoise configuration - define complete MIDDLEWARE list for production
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise early
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

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

# Allow all hosts for Railway - including health check domains
ALLOWED_HOSTS = [
    '*',  # Allow all hosts
    'localhost',
    '127.0.0.1',
    '.railway.app',
    'healthcheck.railway.app',  # Specific health check domain
    '.up.railway.app',  # Railway app domains
]

# Add Railway-specific hosts from environment
railway_static_url = os.environ.get('RAILWAY_STATIC_URL', '')
railway_public_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')

if railway_static_url:
    ALLOWED_HOSTS.append(railway_static_url)
    print(f"📡 Added RAILWAY_STATIC_URL to ALLOWED_HOSTS: {railway_static_url}")

if railway_public_domain:
    ALLOWED_HOSTS.append(railway_public_domain)
    print(f"📡 Added RAILWAY_PUBLIC_DOMAIN to ALLOWED_HOSTS: {railway_public_domain}")

print(f"🌐 ALLOWED_HOSTS: {ALLOWED_HOSTS}")

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

# Security settings for production - but allow health checks
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # Disable for Railway health checks
    SECURE_HSTS_SECONDS = 0  # Disable HSTS for Railway health checks
    SECURE_REDIRECT_EXEMPT = ['/health/']  # Exempt health check from redirects
    SECURE_SSL_REDIRECT = False  # Disable SSL redirect for Railway health checks
    SESSION_COOKIE_SECURE = False  # Allow non-HTTPS for health checks
    CSRF_COOKIE_SECURE = False  # Allow non-HTTPS for health checks
    
    print("🔒 Security settings configured for Railway health checks")

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

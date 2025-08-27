#!/usr/bin/env python3
"""
UniShowTime Project Verification Script
This script verifies the project structure and configuration for Railway deployment.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print result."""
    exists = os.path.exists(file_path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {file_path}")
    return exists

def check_directory_structure():
    """Verify the project directory structure."""
    print("🔍 Checking Project Directory Structure...")
    print("=" * 50)
    
    base_dir = Path(".")
    required_files = [
        ("manage.py", "Django management script"),
        ("requirements.txt", "Python dependencies"),
        ("Dockerfile", "Docker configuration"),
        (".dockerignore", "Docker ignore file"),
        ("railway.toml", "Railway configuration"),
        (".env.example", "Environment variables example"),
        ("UniShowTime/settings.py", "Django settings"),
        ("UniShowTime/production_settings.py", "Production settings"),
        ("UniShowTime/wsgi.py", "WSGI application"),
        ("mainapp/models.py", "Django models"),
        ("mainapp/views.py", "Django views"),
        ("mainapp/urls.py", "Django URLs"),
    ]
    
    all_exist = True
    for file_path, description in required_files:
        exists = check_file_exists(file_path, description)
        if not exists:
            all_exist = False
    
    print("\n" + "=" * 50)
    if all_exist:
        print("✅ All required files are present!")
    else:
        print("❌ Some required files are missing!")
    
    return all_exist

def check_requirements():
    """Check if requirements.txt has necessary dependencies."""
    print("\n🔍 Checking Requirements...")
    print("=" * 50)
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        required_packages = [
            "Django",
            "gunicorn",
            "whitenoise",
            "psycopg2-binary",
            "dj-database-url",
            "python-decouple",
            "Pillow",
            "qrcode"
        ]
        
        missing_packages = []
        for package in required_packages:
            if package.lower() not in content.lower():
                missing_packages.append(package)
        
        if not missing_packages:
            print("✅ All required packages are in requirements.txt")
            return True
        else:
            print("❌ Missing packages in requirements.txt:")
            for package in missing_packages:
                print(f"   - {package}")
            return False
            
    except FileNotFoundError:
        print("❌ requirements.txt not found!")
        return False

def check_docker_config():
    """Check Docker configuration."""
    print("\n🔍 Checking Docker Configuration...")
    print("=" * 50)
    
    try:
        with open("Dockerfile", "r") as f:
            dockerfile_content = f.read()
        
        required_elements = [
            ("FROM python:", "Base Python image"),
            ("WORKDIR /app", "Working directory set"),
            ("COPY requirements.txt", "Requirements copied"),
            ("RUN pip install", "Dependencies installed"),
            ("EXPOSE 8000", "Port exposed"),
            ("gunicorn", "Gunicorn command")
        ]
        
        all_present = True
        for element, description in required_elements:
            if element in dockerfile_content:
                print(f"✅ {description}")
            else:
                print(f"❌ Missing: {description}")
                all_present = False
        
        return all_present
        
    except FileNotFoundError:
        print("❌ Dockerfile not found!")
        return False

def check_settings():
    """Check Django settings configuration."""
    print("\n🔍 Checking Django Settings...")
    print("=" * 50)
    
    issues = []
    
    # Check main settings.py
    try:
        with open("UniShowTime/settings.py", "r") as f:
            settings_content = f.read()
        
        if "RAILWAY_ENVIRONMENT" in settings_content:
            print("✅ Railway environment detection configured")
        else:
            issues.append("Railway environment detection not configured")
        
        if "AUTH_USER_MODEL" in settings_content:
            print("✅ Custom user model configured")
        else:
            issues.append("Custom user model not configured")
            
    except FileNotFoundError:
        issues.append("settings.py not found")
    
    # Check production settings
    try:
        with open("UniShowTime/production_settings.py", "r") as f:
            prod_settings = f.read()
        
        if "dj_database_url" in prod_settings:
            print("✅ Database URL configuration present")
        else:
            issues.append("Database URL configuration missing")
            
        if "WhiteNoise" in prod_settings:
            print("✅ WhiteNoise static files configuration present")
        else:
            issues.append("WhiteNoise configuration missing")
            
    except FileNotFoundError:
        issues.append("production_settings.py not found")
    
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Settings configuration looks good!")
        return True

def generate_deployment_checklist():
    """Generate a deployment checklist."""
    print("\n📋 Railway Deployment Checklist:")
    print("=" * 50)
    
    checklist = [
        "1. Create Railway account at railway.app",
        "2. Connect your GitHub repository to Railway",
        "3. Add PostgreSQL database service",
        "4. Set environment variables in Railway dashboard:",
        "   - SECRET_KEY (generate a new one)",
        "   - DEBUG=False",
        "   - DATABASE_URL (auto-generated by Railway)",
        "   - EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS",
        "   - EMAIL_HOST_USER, EMAIL_HOST_PASSWORD",
        "5. Deploy the application",
        "6. Check Railway logs for any errors",
        "7. Create superuser via Railway shell",
        "8. Test the application functionality"
    ]
    
    for item in checklist:
        print(f"☐ {item}")

def main():
    """Main verification function."""
    print("🚀 UniShowTime Railway Deployment Verification")
    print("=" * 50)
    print("This script checks if your project is ready for Railway deployment with Docker.\n")
    
    # Run all checks
    structure_ok = check_directory_structure()
    requirements_ok = check_requirements()
    docker_ok = check_docker_config()
    settings_ok = check_settings()
    
    # Overall result
    print("\n" + "=" * 50)
    print("📊 OVERALL RESULT")
    print("=" * 50)
    
    if all([structure_ok, requirements_ok, docker_ok, settings_ok]):
        print("🎉 Your project is ready for Railway deployment!")
        print("✅ All checks passed successfully.")
    else:
        print("⚠️  Your project needs some fixes before deployment.")
        print("❌ Please address the issues mentioned above.")
    
    # Show deployment checklist
    generate_deployment_checklist()
    
    print("\n🔗 Useful Links:")
    print("- Railway Docs: https://docs.railway.app")
    print("- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/")
    print("- Docker Best Practices: https://docs.docker.com/develop/best-practices/")

if __name__ == "__main__":
    main()

# 🚀 GitHub Deployment Guide for UniShowTime

This guide will help you push your UniShowTime project to GitHub and set up various deployment options from GitHub.

## 📋 Table of Contents
1. [Initialize Git Repository](#initialize-git-repository)
2. [Push to GitHub](#push-to-github)
3. [GitHub Actions for CI/CD](#github-actions-for-cicd)
4. [Deploy from GitHub](#deploy-from-github)
5. [GitHub Pages (Static Demo)](#github-pages-static-demo)
6. [Branch Management](#branch-management)

## 🔧 Initialize Git Repository

### 1. Check Git Status
First, let's check if Git is already initialized:

```bash
cd /path/to/UniShowTime-main
git status
```

### 2. Initialize Git (if not already done)
```bash
# Initialize git repository
git init

# Add all files
git add .

# Check what will be committed
git status

# Make initial commit
git commit -m "Initial commit: UniShowTime Django project with Railway deployment"
```

### 3. Remove Sensitive Data
Make sure sensitive information is not committed:

```bash
# Check if .env file exists and remove it
rm -f .env

# Ensure .gitignore is working
git status  # Should not show .env, __pycache__, etc.
```

## 🌐 Push to GitHub

### 1. Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click "New repository" (green button)
3. Repository name: `UniShowTime` or `unishowtime`
4. Description: `🎬 University Event Management Platform with Django & QR Code Ticketing`
5. Make it **Public** (recommended for deployment platforms)
6. **Don't** initialize with README, .gitignore, or license (we already have them)
7. Click "Create repository"

### 2. Connect Local Repository to GitHub
```bash
# Add GitHub remote origin
git remote add origin https://github.com/YOUR_USERNAME/UniShowTime.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Verify Upload
- Go to your GitHub repository
- Check that all files are uploaded
- Verify README.md displays correctly

## 🔄 GitHub Actions for CI/CD

Create automated deployment pipeline:

### 1. Create GitHub Actions Workflow
```bash
mkdir -p .github/workflows
```

### 2. Django CI Workflow
Create `.github/workflows/django.yml`:

```yaml
name: Django CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: unishowtime_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run tests
      env:
        SECRET_KEY: 'test-secret-key'
        DEBUG: True
        DATABASE_URL: 'postgresql://postgres:postgres@localhost:5432/unishowtime_test'
      run: |
        python manage.py test
        
    - name: Check Django deployment readiness
      env:
        SECRET_KEY: 'test-secret-key'
        DEBUG: False
        DATABASE_URL: 'postgresql://postgres:postgres@localhost:5432/unishowtime_test'
      run: |
        python manage.py check --deploy --fail-level WARNING
```

### 3. Docker Build Workflow
Create `.github/workflows/docker.yml`:

```yaml
name: Docker Build

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
      
    - name: Build Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        file: ./Dockerfile
        push: false
        tags: unishowtime:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## 🚀 Deploy from GitHub

### 1. Railway Deployment from GitHub

**Steps:**
1. Go to [Railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `UniShowTime` repository
6. Railway automatically detects the `railway.toml` file
7. Add PostgreSQL database service
8. Set environment variables
9. Deploy automatically

**Environment Variables for Railway:**
```
SECRET_KEY=your-generated-secret-key
DEBUG=False
DATABASE_URL=postgresql://... (auto-generated)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 2. Heroku Deployment from GitHub

**Preparation:**
Create `Procfile`:
```
web: gunicorn UniShowTime.wsgi:application
release: python manage.py migrate
```

Create `runtime.txt`:
```
python-3.11.6
```

**Deploy Steps:**
1. Go to [Heroku Dashboard](https://dashboard.heroku.com)
2. Create new app
3. Connect to GitHub repository
4. Enable automatic deployments
5. Add Heroku Postgres add-on
6. Set environment variables
7. Deploy

### 3. DigitalOcean App Platform

**Steps:**
1. Go to [DigitalOcean Apps](https://cloud.digitalocean.com/apps)
2. Create new app from GitHub
3. Select your repository
4. DigitalOcean detects Dockerfile automatically
5. Add managed PostgreSQL database
6. Configure environment variables
7. Deploy

### 4. Vercel (for Static Demo)

For a static demo version:
1. Fork the repository
2. Connect to [Vercel](https://vercel.com)
3. Deploy as static site (templates only)

## 📄 GitHub Pages (Static Demo)

Create a static demo of your app's UI:

### 1. Create GitHub Pages Branch
```bash
# Create and switch to gh-pages branch
git checkout -b gh-pages

# Create a simple index.html for demo
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>UniShowTime - University Event Management</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold text-center text-blue-600 mb-8">
            🎬 UniShowTime
        </h1>
        <p class="text-center text-gray-600 mb-8">
            University Event Management Platform with Django & QR Code Ticketing
        </p>
        
        <div class="grid md:grid-cols-3 gap-6">
            <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-xl font-semibold mb-4">🎟️ Event Management</h3>
                <p>Create and manage university events with ease.</p>
            </div>
            <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-xl font-semibold mb-4">🔑 QR Code Tickets</h3>
                <p>Secure ticket generation with QR codes for entry validation.</p>
            </div>
            <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-xl font-semibold mb-4">💡 Event Suggestions</h3>
                <p>Students can suggest events; admins can approve them.</p>
            </div>
        </div>
        
        <div class="text-center mt-8">
            <a href="https://github.com/YOUR_USERNAME/UniShowTime" 
               class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
                View on GitHub
            </a>
        </div>
    </div>
</body>
</html>
EOF

# Commit and push
git add index.html
git commit -m "Add GitHub Pages demo"
git push origin gh-pages
```

### 2. Enable GitHub Pages
1. Go to repository Settings
2. Scroll to "Pages" section
3. Source: "Deploy from a branch"
4. Branch: `gh-pages`
5. Folder: `/ (root)`
6. Save

Your demo will be available at: `https://yourusername.github.io/UniShowTime`

## 🌿 Branch Management

### Recommended Branch Structure

```bash
# Main branches
main          # Production-ready code
develop       # Development integration
feature/*     # Feature development
hotfix/*      # Critical bug fixes
release/*     # Release preparation

# Create development branch
git checkout -b develop
git push origin develop

# Feature branch example
git checkout develop
git checkout -b feature/user-authentication
# ... make changes ...
git add .
git commit -m "Add user authentication system"
git push origin feature/user-authentication
# Create pull request on GitHub
```

### Git Workflow Commands

```bash
# Update your local repository
git fetch origin
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Stage and commit changes
git add .
git commit -m "Descriptive commit message"

# Push feature branch
git push origin feature/your-feature-name

# Merge back to main (via GitHub PR)
# After PR approval and merge, clean up:
git checkout main
git pull origin main
git branch -d feature/your-feature-name
```

## 🔒 Security Best Practices

### 1. Environment Variables
Never commit sensitive data:

```bash
# Check for sensitive data before commit
git log --oneline | head -10
git show --name-only

# If you accidentally committed sensitive data:
# 1. Remove it from the file
# 2. Commit the fix
# 3. Consider the data compromised and change it
```

### 2. GitHub Security Features

Enable in repository settings:
- [ ] Vulnerability alerts
- [ ] Security advisories
- [ ] Dependency graph
- [ ] Dependabot alerts
- [ ] Secret scanning

### 3. Branch Protection Rules

For `main` branch:
- [ ] Require pull request reviews
- [ ] Require status checks to pass
- [ ] Require up-to-date branches
- [ ] Include administrators

## 📊 Repository Maintenance

### 1. README Badges
Add status badges to your README:

```markdown
![Django CI](https://github.com/YOUR_USERNAME/UniShowTime/workflows/Django%20CI/badge.svg)
![Docker Build](https://github.com/YOUR_USERNAME/UniShowTime/workflows/Docker%20Build/badge.svg)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/UniShowTime)
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/UniShowTime)
```

### 2. Issues and Project Management
- Use GitHub Issues for bug tracking
- Create issue templates
- Use GitHub Projects for project management
- Add labels for categorization

### 3. Documentation
Keep documentation updated:
- README.md (overview)
- CONTRIBUTING.md (contribution guidelines)
- docs/ folder for detailed documentation
- Wiki for extended documentation

## 🎯 Deployment Checklist

Before deploying:

- [ ] Environment variables configured
- [ ] Database settings updated
- [ ] Static files configuration
- [ ] Security settings enabled
- [ ] Error logging configured
- [ ] Backup strategy planned
- [ ] Domain name configured (if custom)
- [ ] SSL certificate enabled
- [ ] Performance monitoring setup

## 🔗 Useful GitHub Repository Links

After pushing to GitHub:

- **Repository**: `https://github.com/YOUR_USERNAME/UniShowTime`
- **Issues**: `https://github.com/YOUR_USERNAME/UniShowTime/issues`
- **Actions**: `https://github.com/YOUR_USERNAME/UniShowTime/actions`
- **Releases**: `https://github.com/YOUR_USERNAME/UniShowTime/releases`
- **Insights**: `https://github.com/YOUR_USERNAME/UniShowTime/pulse`

---

🎉 **Congratulations!** Your UniShowTime project is now on GitHub and ready for cloud deployment from multiple platforms!

## Next Steps:
1. Follow this guide to push to GitHub
2. Choose a deployment platform (Railway recommended)
3. Set up automated deployments
4. Monitor and maintain your application

Happy coding! 🚀

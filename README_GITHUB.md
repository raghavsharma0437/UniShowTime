# 🎬 UniShowTime - University Event Management Platform

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-131415?style=for-the-badge&logo=railway&logoColor=white)

UniShowTime is a comprehensive **Django-based event management and ticketing platform** designed specifically for universities. It empowers students to explore events, book tickets with QR codes, suggest new events, and helps administrators manage campus activities efficiently.

## ✨ Features

- 🎟️ **Event Creation & Management** – Organizers can create, edit, and manage university events
- 👥 **Multi-Role System** – Students, Event Admins, and Super Admins with different permissions
- 🔑 **QR Code Tickets** – Secure, scannable QR codes for event entry validation
- 💡 **Event Suggestions** – Students can suggest events; admins can review and approve them
- 📷 **Event Memories** – Photo galleries and memories from past events
- 🏫 **Department Management** – Organize events by university departments
- 📊 **Admin Dashboard** – Comprehensive analytics, logs, and system management
- 🎨 **Modern UI** – Responsive design with TailwindCSS
- 📱 **Mobile Friendly** – Optimized for all devices
- 🔒 **Secure Authentication** – Custom user model with role-based access control

## 🛠️ Tech Stack

- **Backend**: Django 5.1+ (Python)
- **Frontend**: Django Templates + TailwindCSS
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Django's Custom User Model
- **QR Generation**: Python qrcode library
- **Deployment**: Docker + Railway/Heroku
- **Static Files**: WhiteNoise + Django Compressor
- **WSGI Server**: Gunicorn

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- Docker (for containerized deployment)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/UniShowTime.git
cd UniShowTime
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 🐳 Docker Deployment

### Local Development with Docker
```bash
# Build and run with docker-compose
docker-compose up --build

# Access at http://localhost:8000
```

### Production Deployment
```bash
# Build Docker image
docker build -t unishowtime .

# Run container
docker run -p 8000:8000 unishowtime
```

## ☁️ Cloud Deployment

### Railway (Recommended)
1. Fork this repository
2. Connect to [Railway](https://railway.app)
3. Add PostgreSQL database
4. Set environment variables
5. Deploy automatically

**📖 Detailed Guide**: See [RAILWAY_DEPLOYMENT_GUIDE.md](RAILWAY_DEPLOYMENT_GUIDE.md)

### Other Platforms
- **Heroku**: Supports Django + PostgreSQL
- **DigitalOcean App Platform**: Docker-based deployment
- **AWS EC2**: Full control deployment
- **Google Cloud Run**: Serverless container deployment

## 🔧 Configuration

### Environment Variables
```env
SECRET_KEY=your-django-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:5432/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Key Settings
- **Custom User Model**: `mainapp.CustomUser`
- **Media Files**: Uploaded to `media/` directory
- **Static Files**: Collected to `staticfiles/` for production
- **Authentication**: Role-based (Student, Admin, Super Admin)

## 👥 User Roles

### 🎓 Students
- Browse and view events
- Book tickets with QR codes
- Suggest new events
- View event memories
- Manage profile

### 👨‍💼 Event Admins
- Create and manage events
- View event analytics
- Manage event attendees
- Upload event photos

### 🔑 Super Admins
- Full system access
- User management
- Department management
- System logs and backups
- Platform configuration

## 📱 Key Features Walkthrough

### Event Management
- Create events with details, images, and ticket limits
- Set pricing and availability
- Manage attendee lists
- Upload event memories

### QR Code Ticketing
- Automatic QR code generation for tickets
- Secure validation system
- Mobile-friendly scanning
- Ticket download functionality

### Event Suggestions
- Student-driven event suggestions
- Admin review and approval workflow
- Convert suggestions to real events

## 🛡️ Security Features

- CSRF protection enabled
- Secure password validation
- Role-based access control
- SQL injection protection
- XSS protection headers
- HTTPS enforcement (production)

## 📊 System Administration

### Backup & Restore
- Automated system backups
- Database export functionality
- Media file management

### Logging & Monitoring
- Comprehensive system logs
- User activity tracking
- Error monitoring
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guide
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📋 Project Structure

```
UniShowTime/
├── 📁 UniShowTime/          # Django project settings
│   ├── settings.py          # Main settings
│   ├── production_settings.py  # Production configuration
│   ├── urls.py             # URL configuration
│   └── wsgi.py             # WSGI application
├── 📁 mainapp/             # Main Django application
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Django forms
│   ├── urls.py             # App URLs
│   └── templates/          # HTML templates
├── 📁 media/               # User uploaded files
├── 📁 static/              # Static assets
├── 📁 scripts/             # Utility scripts
├── 🐳 Dockerfile           # Docker configuration
├── 🚂 railway.toml         # Railway deployment
├── 📋 requirements.txt     # Python dependencies
└── 📖 README.md           # This file
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📈 Performance

- **Database**: Optimized queries with select_related/prefetch_related
- **Static Files**: Compressed and cached with WhiteNoise
- **Images**: Pillow-based image processing
- **Caching**: Django's caching framework ready
- **CDN Ready**: Static files can be served via CDN

## 🔗 API Integration

The platform is designed to be extended with REST APIs:
- Django REST Framework compatible
- JWT authentication ready
- Mobile app integration possible

## 📱 Mobile Support

- Responsive design works on all devices
- QR code scanning optimized for mobile
- Touch-friendly interface
- Progressive Web App (PWA) ready

## 🌐 Internationalization

- Translation-ready codebase
- Multiple language support possible
- Timezone handling included

## 📞 Support

- **Documentation**: Comprehensive guides included
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Email**: Contact maintainers for urgent issues

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the amazing framework
- TailwindCSS for the utility-first CSS framework
- Railway for simplified deployment
- University community for testing and feedback

## 🔄 Version History

- **v1.0.0** - Initial release with core features
- **v1.1.0** - Added Docker support and Railway deployment
- **v1.2.0** - Enhanced security and performance optimizations

---

<div align="center">

**🎉 Built with ❤️ for the university community**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/UniShowTime?style=social)](https://github.com/yourusername/UniShowTime)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/UniShowTime?style=social)](https://github.com/yourusername/UniShowTime)

</div>

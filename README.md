# Swahilipot Foundation Portal

> A modern, secure, scalable, and production-ready Django platform designed to digitize and streamline operations at the Swahilipot Foundation.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/github/license/MissMolly037/swahilipot-foundation-portal)

---

## 🌟 Project Highlights

- 🐳 Docker & Docker Compose support
- 🗄 PostgreSQL production-ready configuration
- 🔐 Secure authentication and role-based access control
- 📍 GPS-based attendance tracking with geofencing
- 🎫 QR code event check-in
- 📱 Progressive Web App (PWA)
- 📊 Interactive analytics dashboard
- ⚙️ GitHub Actions continuous integration
- 🛡 WhiteNoise static file serving
- 🚀 Production-ready deployment architecture

# 📖 Overview

The **Swahilipot Foundation Portal** is a comprehensive Django-based web application developed to modernize and digitize the daily operations of the Swahilipot Foundation.

The platform replaces manual workflows with a secure, centralized system for managing users, attendance, communication, events, tasks, and organizational resources.

Designed with scalability, maintainability, and security in mind, the project demonstrates modern Django development practices including Docker containerization, PostgreSQL support, GitHub Actions, and production-ready deployment.

---

# 📑 Table of Contents

- [Features](#-features)
- [System Modules](#-system-modules)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Docker Setup](#-docker-setup)
- [Environment Variables](#-environment-variables)
- [Running Tests](#-running-tests)
- [Security Features](#-security-features)
- [Screenshots](#-screenshots)
- [Architecture](#-architecture)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Documentation](#-documentation)
- [License](#-license)

---

# ✨ Features

- 🔐 Secure Authentication & Authorization
- 👥 User & Department Management
- 📊 Interactive Dashboard
- 📍 GPS Attendance Tracking with Geofencing
- 📅 Event Management
- 🎫 QR Code Event Check-in
- 📢 Internal Communication & Notifications
- ✅ Task Management
- 💡 Suggestions & Feedback
- 📈 Reports & Analytics
- 📱 Responsive Design
- 🌐 Progressive Web App (PWA)
- 🔔 Push Notifications
- 🔒 Role-Based Access Control
- 🐳 Docker Support
- 🗄 PostgreSQL Support

---

# 🏗 System Modules

| Module | Description |
|---------|-------------|
| Accounts | User authentication, profiles and permissions |
| Dashboard | Analytics, summaries and reporting |
| Attendance | Check-in, check-out, geofencing and attendance reports |
| Events | Event management, registration and QR code check-in |
| Communication | Internal messaging and notifications |
| Tasks | Task assignment and tracking |
| Suggestions | Suggestion and feedback management |
| Core | Shared utilities, permissions and reporting |

---

# 🛠 Technology Stack

## Backend

- Python 3.12
- Django 6
- Gunicorn
- WhiteNoise

## Database

- SQLite (Development)
- PostgreSQL (Production)

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## Infrastructure

- Docker
- Docker Compose
- GitHub Actions

## Additional Technologies

- Progressive Web App (PWA)
- QR Code Generation
- Google Forms Integration
- Push Notifications

---

# 📂 Project Structure

```
swahilipot-foundation-portal/
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
│
├── accounts/
├── attendance/
├── communication/
├── core/
├── dashboard/
├── events/
├── suggestions/
├── tasks/
│
├── templates/
├── static/
├── media/
├── docs/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── README.md
└── LICENSE
```

---

# 🚀 Quick Start

## Clone the repository

```bash
git clone https://github.com/MissMolly037/swahilipot-foundation-portal.git
cd swahilipot-foundation-portal
```

## Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Apply migrations

```bash
python manage.py migrate
```

## Create a superuser

```bash
python manage.py createsuperuser
```

## Run the development server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000
```

---

# 🐳 Docker Setup

Build the Docker image:

```bash
docker compose build
```

Start the application:

```bash
docker compose up -d
```

View running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop the application:

```bash
docker compose down
```

Access the application:

```
http://localhost:8000
```

---

# ⚙️ Environment Variables

Create a `.env` file:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False

POSTGRES_DB=swahilipot
POSTGRES_USER=swahilipot
POSTGRES_PASSWORD=swahilipot
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

---

# 🧪 Running Tests

Run all tests:

```bash
python manage.py test
```

Run a specific app:

```bash
python manage.py test accounts.tests
```

---

# 🔒 Security Features

- Django Authentication
- Role-Based Access Control
- CSRF Protection
- Session Security
- Password Hashing
- Environment Variable Configuration
- WhiteNoise Static File Security
- Security Middleware
- Production-Ready Docker Configuration

---

# 📸 Screenshots

Screenshots will be added in the next release.

Planned screenshots include:

- Login Page
- Dashboard
- Attendance Module
- Event Management
- QR Code Check-in
- Task Management
- Reports Dashboard

---

# 🏗 Architecture

```
                Users
                  │
                  ▼
            Web Browser
                  │
                  ▼
         Docker Container
                  │
                  ▼
        Gunicorn + Django
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
 WhiteNoise              PostgreSQL
Static Files              Database
```

---

# 📊 Project Status

| Component | Status |
|-----------|--------|
| Django Application | ✅ Complete |
| Docker Support | ✅ Complete |
| PostgreSQL Support | ✅ Complete |
| CI/CD Pipeline | 🚧 In Progress |
| Production Deployment | 🚧 Planned |
| Documentation | 🚧 Improving |

---

# 📈 Roadmap

Upcoming improvements include:

- REST API
- Cloud Deployment
- CI/CD Pipeline
- Email Notifications
- SMS Notifications
- Advanced Analytics
- Mobile Application
- Calendar Integration
- Multi-Organization Support

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push your branch

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

Please ensure all tests pass before submitting your pull request.

---

# 📚 Documentation

Additional documentation included in this repository:

- `CHANGELOG.md`
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `ROADMAP.md`
- `SECURITY.md`

Future documentation will be available in the `docs/` directory.

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

# 👩‍💻 Author

**Margaret Wambui Njaaga**

Software Engineering Student | Python Developer | Django Developer

- **GitHub:** https://github.com/MissMolly037
- **Project Repository:** https://github.com/MissMolly037/swahilipot-foundation-portal

---

## 🙏 Acknowledgements

This project was developed as part of my software engineering portfolio to demonstrate modern Django development practices, including Docker, PostgreSQL, GitHub Actions, and production-ready deployment.
---

# ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.

Your support helps improve the project and encourages future development.
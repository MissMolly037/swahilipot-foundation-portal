# Swahilipot Foundation Portal

> A modern, secure, and scalable Django-based portal designed to digitize and streamline operations at the Swahilipot Foundation.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-6.0-success)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Overview

The **Swahilipot Foundation Portal** is a comprehensive web application developed using **Django** to modernize the management of foundation activities.

The system replaces manual workflows with a secure, centralized platform that enables efficient management of users, attendance, events, communication, tasks, and organizational resources.

The portal has been designed with scalability, security, and ease of use in mind, making it suitable for nonprofit organizations, training institutions, and community hubs.

---

# ✨ Features

- 🔐 Secure Authentication & Authorization
- 👥 User & Department Management
- 📊 Interactive Dashboard
- 📍 Attendance Tracking with Geofencing
- 📅 Event Management
- 🎫 QR Code Event Check-in
- 📢 Internal Communication & Notifications
- ✅ Task Management
- 💡 Suggestions & Feedback Management
- 📈 Reports & Analytics
- 📱 Responsive Mobile-Friendly Design
- 🌐 Progressive Web App (PWA) Support
- 🔔 Push Notifications
- 🔒 Role-Based Access Control

---

# 🏗 System Modules

| Module | Description |
|---------|-------------|
| Accounts | User authentication, profiles and permissions |
| Dashboard | Overview of system activities and reports |
| Attendance | Check-in, check-out, geofencing and attendance reports |
| Events | Event management, registrations and QR code check-in |
| Communication | Notifications and internal messaging |
| Tasks | Task assignment and tracking |
| Suggestions | Suggestion and feedback management |
| Core | Shared utilities, permissions and reporting |

---

# 🛠 Technology Stack

## Backend

- Python 3.12
- Django 6
- SQLite (Development)
- PostgreSQL (Production Ready)

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## Additional Technologies

- Progressive Web App (PWA)
- Service Workers
- Web Push Notifications
- QR Code Generation
- Google Forms Integration

## Development Tools

- Git
- GitHub
- GitHub Actions
- Visual Studio Code

---

# 📂 Project Structure

```
swahilipot-foundation-portal/
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
│       └── django-tests.yml
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
│
├── manage.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# 🚀 Installation

## Clone the repository

```bash
git clone https://github.com/MissMolly037/swahilipot-foundation-portal.git
```

## Navigate into the project

```bash
cd swahilipot-foundation-portal
```

## Create a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install project dependencies

```bash
pip install -r requirements.txt
```

## Apply database migrations

```bash
python manage.py migrate
```

## Create a superuser (optional)

```bash
python manage.py createsuperuser
```

## Run the development server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

---

# 🧪 Running Tests

Run all tests

```bash
python manage.py test
```

Run a specific test module

```bash
python manage.py test accounts.tests
```

---

# 🔒 Security Features

- Django Authentication
- Role-Based Access Control
- CSRF Protection
- Secure Password Hashing
- Session Management
- Environment Variable Configuration
- Security Middleware
- Protected Administrative Functions

---

# 📸 Screenshots

The following screenshots will be added in future releases:

- Login Page
- Dashboard
- Attendance Management
- Event Registration
- QR Code Check-in
- User Management
- Reports Dashboard

---

# 📈 Roadmap

Future enhancements include:

- REST API
- Docker Deployment
- PostgreSQL Production Deployment
- Email Notifications
- SMS Notifications
- Advanced Analytics Dashboard
- Mobile Application
- Calendar Integration
- Multi-Organization Support

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository

2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

Please ensure all tests pass before submitting a pull request.

---

# 📜 Project Documentation

Additional documentation included in this repository:

- CONTRIBUTING.md
- CHANGELOG.md
- CODE_OF_CONDUCT.md
- ROADMAP.md
- SECURITY.md

---

# 📄 License

This project is licensed under the **MIT License**.

See the **LICENSE** file for more information.

---

# 👩‍💻 Author

**Margaret Wambui Njaaga**

Aspiring Software Engineer

GitHub:
https://github.com/MissMolly037

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

Your support helps improve the project and encourages future development.
# Swahilipot Foundation Portal

A modern web-based management platform designed for **Swahilipot Foundation** to streamline organizational operations, member management, attendance tracking, communication, event coordination, and reporting.

---

## 📖 Overview

The **Swahilipot Foundation Portal** is built using **Django** and provides a centralized system that enables administrators, staff, and members to efficiently manage daily organizational activities through a secure and user-friendly interface.

The platform is designed to improve operational efficiency, transparency, collaboration, and digital transformation within the foundation.

---

## ✨ Features

- 🔐 Secure User Authentication
- 👥 User & Role Management
- 📅 Attendance Tracking
- 🎉 Event Management
- 📋 Task Management
- 💬 Internal Communication
- 💡 Suggestion Box
- 📊 Dashboard & Reports
- 📝 Google Forms Integration
- 📧 Email Notifications
- 📁 Document & Resource Management
- 📱 Responsive User Interface

---

## 🏗️ Project Structure

```text
swahilipot-foundation-portal/
│
├── accounts/
├── attendance/
├── communication/
├── core/
├── dashboard/
├── events/
├── suggestions/
├── tasks/
├── static/
├── templates/
├── swahilipot_portal/
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Technology Stack

### Backend

- Python
- Django

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap

### Database

- SQLite (Development)

### Deployment

- PythonAnywhere

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/MissMolly037/swahilipot-foundation-portal.git
```

### Navigate into the project

```bash
cd swahilipot-foundation-portal
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Start the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## ⚙️ Environment Variables

Create a `.env` file using the provided `.env.example` file.

Example:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 📸 Screenshots

Project screenshots will be added as the system continues to evolve.

---

## 🗺️ Roadmap

- Docker Support
- REST API
- Progressive Web App (PWA)
- Automated Testing
- GitHub Actions (CI/CD)
- Performance Optimization
- Analytics Dashboard
- Mobile Integration

---

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome.

Please fork the repository, create a feature branch, and submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author

**Margaret Wambui Njaaga**

- GitHub: https://github.com/MissMolly037

---

## 🌍 About Swahilipot Foundation

Swahilipot Foundation is a youth-focused innovation hub dedicated to empowering young people through technology, creativity, entrepreneurship, and community development. This portal supports the foundation's digital operations by providing a centralized platform for managing organizational activities efficiently.

# ISP OLT Automation System

This project aims to automate various tasks for Internet Service Providers (ISPs) by integrating with MikroTik routers and OLT (Optical Line Terminal) devices.

## Features

- Web-based system with user login.
- Add and manage MikroTik and OLT devices.
- Display ONU/User status (online/offline, signal levels) by searching username.
- Dedicated page to view and manage offline ONUs.
- Option to remove offline ONUs from the OLT directly from the web interface.

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL
- **Network Automation:** Netmiko, MikroTik API
- **Version Control:** Git, GitHub

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [your_github_repository_url](https://github.com/alamin2025k/isp_olt_automation_system.git)
    cd isp_automation_system
    ```
2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Create `.env` file:**
    Copy `.env.example` to `.env` and fill in your database credentials and Django SECRET_KEY.
    ```
    cp .env.example .env
    ```
4.  **Database Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5.  **Create a Superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    Access the application at `http://127.0.0.1:8000`.

## Configuration

All device credentials and sensitive settings are managed through the web interface.

---

# School Portal Application

A responsive web-based school portal built using Python and NiceGUI. This application features a role-based login system for Administrators and Teachers, custom student/staff data insertion tools, database backup utilities, and activity logging backed by a local SQLite database.

## Features

* **Role-Based Routing:** Auto-redirects to administrative dashboards or teacher management pages depending on user privileges.
* **Secure Authentication:** User registration, password resets, and login portals integrated with password hashing mechanisms.
* **Automated Backups:** Dedicated backup utilities (`backup.py`) to safeguard database files and prevent data loss.
* **Activity Tracker:** Real-time database logging to track session statuses (`Active` / `Inactive`) and login timestamps.
* **Modern UI:** Responsive grid layout using custom theme styling, Tailwind CSS utilities, and dark-maroon brand accents.

## Tech Stack

* **Frontend/Backend:** NiceGUI (Python-based UI framework)
* **Data Engineering:** Polars (Lightning-fast DataFrame library)
* **Database:** SQLite (Built-in Python SQL database engine)
* **Security:** Bcrypt (Secure password hashing)
* **API Requests:** Requests (HTTP library)

## Project Structure

Ensure your local repository files match this structure before running. Note that GitHub will automatically sort these files alphabetically in your repository view:

```text
├── loginPage.py            # Main entry point & app routing
├── verifying_passcode.py    # Login validation & registration logic
├── school_home_page.py      # Admin / School landing dashboard
├── teacher_page.py          # Teacher portal interface
├── insert.py                # Database insertion utility functions
├── backup.py                # Database backup and maintenance tools
├── school_database.db       # Local SQLite database (Auto-generated)
├── requirements.txt         # External dependencies
└── README.md                # Project documentation
```

## Getting Started

### 1. Clone the Repository
```bash
git clone github.com
cd your-repo-name
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
```

Activate the environment based on your operating system:
* **Windows:** `venv\Scripts\activate`
* **macOS / Linux:** `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python loginPage.py
```
Once started, open your web browser and navigate to: `http://localhost:8080/`

## GitHub Actions CI/CD Pipeline

To ensure dependencies compile correctly and code changes pass checks, save the following code inside your repository as `.github/workflows/ci.yml`:

```yaml
name: Python Application CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Code
      uses: actions/checkout@v5

    # Fixed version targeting Node 24 natively to prevent deprecation warnings
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
```

## Default Admin Accounts

For initial configuration, the system recognizes the following master administrative accounts:

| Username | Default Password |
| :--- | :--- |
| **Apostle** | `password1234` |
| **Principal** | `AdminPass2026` |
| **Headmaster** | `Secret123` |

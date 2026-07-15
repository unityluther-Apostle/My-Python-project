# School Portal Application

A lightweight, responsive web-based school portal built using Python and NiceGUI. This application features a role-based login system for Administrators and Teachers, custom student/staff data insertion tools, and activity logging backed by a local SQLite database.

## 🚀 Features

- **Role-Based Routing:** Auto-redirects to administrative dashboards or teacher management pages depending on user privileges.
- **Secure Authentication:** User registration, password resets, and login portals integrated with password hashing mechanisms.
- **Activity Tracker:** Real-time database logging to track session statuses (`Active` / `Inactive`) and login timestamps.
- **Modern UI:** Responsive grid layout using custom theme styling, Tailwind CSS utilities, and dark-maroon brand accents.

---

## 🛠️ Tech Stack

- **Frontend/Backend:** [NiceGUI](https://nicegui.io) (Python-based UI framework)
- **Data Engineering:** [Polars](https://pola.rs) (Lightning-fast DataFrame library)
- **Database:** SQLite (Built-in Python SQL database engine)
- **Security:** Bcrypt (Secure password hashing)
- **API Requests:** Requests (HTTP library for potential external API hooks)

---

## 📂 Project Structure

Ensure your local repository files match this structure before running:

```text
├── loginPage.py                 # Application entry point & routing
├── verifying_passcode.py    # Login validation & user registration logic
├── school_home_page.py      # Admin / School landing dashboard
├── teacher_page.py          # Teacher portal interface
├── insert.py                # Database insertion utility functions
├── school_database.db       # Local SQLite database (Auto-generated)
├── requirements.txt         # External dependencies
└── README.md                # Project documentation
```

---

## 💻 Getting Started

### 1. Clone the Repository
```bash
git clone github.com
cd YOUR_REPO_NAME
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python main.py
```
Once started, open your web browser and navigate to: `http://localhost:8080/`

---

## 🔑 Default Admin Accounts

For initial configuration, the system recognizes the following master administrative accounts:

| Username | Default Password |
| :--- | :--- |
| **Apostle** | `password1234` |
| **Principal** | `AdminPass2026` |
| **Headmaster** | `Secret123` |

*Note: For production environments, remember to replace these hardcoded dictionary values with dynamic database environment variables.*

# iClinic V.2 - Project Structure

## 📁 Clean Project Organization

```
iClinic V.2/
│
├── 📄 app.py                                    # Main Flask application (all routes & APIs)
├── 📄 run.py                                    # Application runner script
├── 📄 requirements.txt                          # Python dependencies
├── 📄 install_and_run.bat                       # Windows installation script
├── 📄 .gitignore                                # Git ignore rules
│
├── 📄 medical aknowlegement letter.docx         # ⚠️ IMPORTANT: Letter template
│
├── 📁 STUDENT/                                  # Student Interface Pages
│   ├── ST-dashboard.html                        # Student dashboard
│   ├── ST-health-records.html                   # Health records view
│   ├── ST-appointment.html                      # Appointment booking
│   ├── ST-consulatation-chat.html               # Online consultation chat
│   └── ST-Announcement.html                     # View announcements
│
├── 📁 pages/                                    # Staff, Admin & Public Pages
│   ├── admin/                                   # Admin interface
│   │   ├── ADMIN-dashboard.html
│   │   ├── REPORTS.html
│   │   └── USER_MANAGEMENT_NEW.HTML
│   │
│   ├── staff/                                   # Staff interface
│   │   ├── Staff-Dashboard.html
│   │   ├── Staff-Patients.html
│   │   ├── Staff-Appointments.html
│   │   ├── Staff-Consultations.html
│   │   ├── Staff-Inventory.html
│   │   ├── Staff-Reports.html
│   │   └── Staff-Announcement.html
│   │
│   └── public/                                  # Public pages
│       ├── landing-page.html
│       ├── login.html
│       ├── complete-registration.html
│       ├── email-verification.html
│       ├── verification-result.html
│       ├── 404.html
│       └── 500.html
│
├── 📁 assets/                                   # Static Assets
│   ├── css/                                     # Stylesheets
│   │   ├── common.css
│   │   └── libs/
│   ├── js/                                      # JavaScript
│   │   ├── common.js
│   │   └── libs/
│   ├── img/                                     # Images
│   │   ├── iclinic-logo.png
│   │   ├── hero-background.png
│   │   └── New Building.png
│   └── fonts/                                   # Custom fonts
│
├── 📁 config/                                   # Configuration Files
│   ├── database.py                              # Database connection
│   └── sms_notifications.py                     # SMS configuration
│
├── 📁 __pycache__/                              # Python cache (auto-generated)
├── 📁 .venv/                                    # Virtual environment (auto-generated)
│
└── 📄 Documentation Files
    ├── README.md                                # Project overview
    ├── GMAIL_SETUP_GUIDE.md                     # Gmail SMTP setup
    ├── OFFLINE_SETUP_GUIDE.md                   # Offline installation
    ├── SETUP_LETTER_GENERATION.md               # Letter generation setup
    ├── UNIFIED_DASHBOARD_CHANGES.md             # Dashboard unification docs
    └── PROJECT_STRUCTURE.md                     # This file
```

---

## 🎯 Key Files Explained

### Core Application Files

| File | Purpose | Critical? |
|------|---------|-----------|
| `app.py` | Main Flask application with all routes and API endpoints | ✅ YES |
| `run.py` | Script to start the Flask server | ✅ YES |
| `requirements.txt` | Python package dependencies | ✅ YES |
| `medical aknowlegement letter.docx` | Template for generating medical letters | ✅ YES |

### Configuration Files

| File | Purpose |
|------|---------|
| `config/database.py` | MySQL database connection settings |
| `config/sms_notifications.py` | SMS notification configuration |

### Interface Directories

| Directory | Purpose | Users |
|-----------|---------|-------|
| `STUDENT/` | Student portal interface | Students, Teaching Staff, Non-Teaching Staff |
| `pages/staff/` | Staff management interface | Clinic Staff (Nurses) |
| `pages/admin/` | Admin dashboard | System Administrators |
| `pages/public/` | Public-facing pages | All users (login, registration) |

---

## 🗑️ Cleaned Up (Deleted)

The following files were removed as they are not needed for production:

### Test Files (18 files)
- All `test_*.html` and `test_*.py` files
- Used for development testing only

### Debug Scripts (6 files)
- All `debug_*.py` files
- Used for troubleshooting during development

### Check Scripts (8 files)
- All `check_*.py` and `verify_*.py` files
- One-time database verification scripts

### Migration Scripts (3 files)
- `migrate_database.py`, `migrate_to_student_number.sql`, etc.
- Already executed, no longer needed

### Setup Scripts (7 files)
- `add_*.py`, `populate_*.py`, `import_*.py`
- One-time data population scripts

### Batch Files (3 files)
- `*.bat` files (except install_and_run.bat)
- One-time setup scripts

### Other (11 files)
- Empty database files (`clinic.db`, `iclinic.db`)
- Temporary files (`temp_function.txt`)
- Sample data (`Student_Profiles_500.txt`)
- Old scripts (`generate_letter.py` - replaced by integrated version)

### Empty Directories (2 folders)
- `components/` - Empty
- `docs/` - Empty

---

## 📊 Cleanup Summary

- **Files Deleted**: 56
- **Directories Deleted**: 2
- **Files Remaining**: 18 core files + documentation
- **Project Size**: Reduced significantly

---

## 🚀 Running the Application

### Windows
```bash
install_and_run.bat
```

### Manual Start
```bash
# Activate virtual environment
.venv\Scripts\activate

# Run the application
python run.py
```

### Access URLs
- **Landing Page**: http://127.0.0.1:5000/
- **Login**: http://127.0.0.1:5000/login
- **Student Dashboard**: http://127.0.0.1:5000/student/dashboard
- **Staff Dashboard**: http://127.0.0.1:5000/dashboard

---

## ⚠️ Important Notes

1. **DO NOT DELETE** `medical aknowlegement letter.docx` - Required for letter generation system
2. **DO NOT DELETE** `app.py` - Main application file
3. **DO NOT DELETE** `config/` folder - Contains database settings
4. **DO NOT DELETE** `assets/` folder - Contains all CSS, JS, and images

---

## 📝 Maintenance

### Adding New Features
- Add routes to `app.py`
- Create new HTML files in appropriate `pages/` subdirectory
- Update this documentation

### Database Changes
- Modify `config/database.py` for connection settings
- Database schema changes should be done through `app.py` init_db() function

---

**Last Updated**: October 16, 2025  
**Version**: 2.0 (Clean Structure)  
**Status**: ✅ Production Ready

# iClinic - Healthcare Management System

A modern web-based clinic management system designed for educational institutions like Norzagaray College.

## 📁 Project Structure

```
iClini V.2/
├── index.html                 # Main entry point (redirects to landing page)
├── README.md                  # Project documentation
│
├── pages/                     # HTML pages organized by user type
│   ├── public/               # Public-facing pages
│   │   ├── landing-page.html # Main landing/homepage
│   │   └── login.html        # User authentication
│   │
│   └── staff/                # Staff/admin pages
│       ├── clinic_staff_dashboard.html
│       ├── Staff-Appointments.html
│       ├── Staff-Consultations.html
│       ├── Staff-Dashboard.html
│       ├── Staff-Inventory.html
│       ├── Staff-Patients.html
│       ├── Staff-Reports.html
│       └── Staff-Settings.html
│
├── assets/                   # Static assets
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   ├── img/                 # Images and graphics
│   │   ├── iclinic-logo.png
│   │   ├── New Building.png
│   │   └── hero-background.png
│   └── fonts/               # Custom fonts
│
├── components/              # Reusable UI components
├── config/                  # Configuration files
└── docs/                    # Additional documentation
```

## 🚀 Getting Started

1. **Access the Application**
   - Open `index.html` in your web browser
   - Or directly access `pages/public/landing-page.html`

2. **Development Setup**
   - Place the project in your web server directory (e.g., `htdocs` for XAMPP)
   - Ensure all file paths are correctly referenced
   - Test navigation between pages

## 📋 Features

- **Acknowledgment Letter**: Secure student medical profiles
- **Smart Medicine Inventory**: Stock tracking with expiry alerts
- **Student Services**: Online appointments and acknowledgment letter
- **AI & Analytics**: Health statistics and insights
- **24/7 Access**: Web-based platform accessible anywhere

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide Icons
- **Animations**: AOS (Animate On Scroll)
- **Charts**: Chart.js

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile devices

## 🔧 File Organization Benefits

### Before Reorganization
- Files scattered in root directory
- Mixed public and staff files
- No clear separation of concerns
- Difficult to maintain and scale

### After Reorganization
- ✅ Clear separation by user type (`public/` vs `staff/`)
- ✅ Organized assets in dedicated folders
- ✅ Proper entry point with `index.html`
- ✅ Scalable structure for future development
- ✅ Easy to locate and maintain files

## 🔗 Navigation Structure

```
index.html → pages/public/landing-page.html
                ↓
            pages/public/login.html
                ↓
            pages/staff/[various staff pages]
```

## 🎨 Asset Management

- **Images**: Stored in `assets/img/`
- **Stylesheets**: Organized in `assets/css/`
- **Scripts**: Managed in `assets/js/`
- **Fonts**: Custom fonts in `assets/fonts/`

## 📝 Development Guidelines

1. **File Naming**: Use descriptive, lowercase names with hyphens
2. **Asset Paths**: Always use relative paths from file location
3. **Code Organization**: Keep HTML, CSS, and JS separated when possible
4. **Documentation**: Update this README when adding new features

## 🏥 About iClinic

iClinic is designed to modernize healthcare operations in educational institutions, providing:
- Efficient student health management
- Streamlined clinic operations
- Data-driven health insights
- Improved accessibility and user experience

---

**Developed for Norzagaray College**  
*Transforming Student Healthcare Management*

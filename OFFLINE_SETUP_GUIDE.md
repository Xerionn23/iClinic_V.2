# iClinic Offline Setup Guide

Gawin mo itong mga steps para gumana ang iClinic system kahit walang internet:

## Step 1: Run Setup Script
1. Double-click `setup_offline_assets.bat`
2. Makikita mo ang mga folders na na-create

## Step 2: Download Required Files

### Critical Files (Download these first):
1. **Alpine.js** (Most Important)
   - URL: https://unpkg.com/alpinejs@3.13.3/dist/cdn.min.js
   - Save as: `assets\js\libs\alpine.min.js`

2. **Feather Icons** (For icons)
   - URL: https://unpkg.com/feather-icons@4.29.0/dist/feather.min.js
   - Save as: `assets\js\libs\feather.min.js`

### Optional Files (For better styling):
3. **Tailwind CSS**
   - URL: https://unpkg.com/tailwindcss@3.3.0/dist/tailwind.min.css
   - Save as: `assets\css\libs\tailwind.min.css`

4. **AOS Animation CSS**
   - URL: https://unpkg.com/aos@2.3.4/dist/aos.css
   - Save as: `assets\css\libs\aos.css`

5. **AOS Animation JS**
   - URL: https://unpkg.com/aos@2.3.4/dist/aos.js
   - Save as: `assets\js\libs\aos.js`

## Step 3: Update HTML Files

Replace these lines in ALL HTML files:

### Replace Tailwind CSS:
```html
<!-- FROM: -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- TO: -->
<link rel="stylesheet" href="../../assets/css/libs/tailwind.min.css">
```

### Replace Alpine.js:
```html
<!-- FROM: -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- TO: -->
<script defer src="../../assets/js/libs/alpine.min.js"></script>
```

### Replace Feather Icons:
```html
<!-- FROM: -->
<script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>

<!-- TO: -->
<script src="../../assets/js/libs/feather.min.js"></script>
```

### Replace AOS CSS:
```html
<!-- FROM: -->
<link href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" rel="stylesheet">

<!-- TO: -->
<link href="../../assets/css/libs/aos.css" rel="stylesheet">
```

### Replace AOS JS:
```html
<!-- FROM: -->
<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>

<!-- TO: -->
<script src="../../assets/js/libs/aos.js"></script>
```

### Replace Inter Font:
```html
<!-- FROM: -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- TO: -->
<link href="../../assets/css/libs/inter-font.css" rel="stylesheet">
```

## Files to Update:
- `pages/staff/Staff-Dashboard.html`
- `pages/staff/Staff-Patients.html`
- `pages/staff/Staff-Appointments.html`
- `pages/staff/Staff-Consultations.html`
- `pages/staff/Staff-Inventory.html`
- `pages/staff/Staff-Reports.html`
- `pages/public/landing-page.html`
- `pages/public/404.html`
- `pages/public/500.html`
- `index.html`

## Quick Test:
1. Disconnect internet
2. Open any page sa browser
3. Kung gumagana pa rin, success!

## Minimum Requirements for Offline:
- **Alpine.js** - Para sa interactive features
- **Feather Icons** - Para sa mga icons
- **Inter Font CSS** - Para sa fonts (may fallback naman)

## Notes:
- Pwede mo i-skip ang Tailwind kung ayaw mo mag-download ng malaking file
- AOS animations optional lang din
- Ang pinaka-importante ay Alpine.js at Feather Icons

## Troubleshooting:
- Kung hindi pa rin gumagana, check mo kung tama ang file paths
- Make sure na naka-save ang files sa tamang location
- Check browser console for errors (F12)
# 📧 iClinic Inventory Notification System

## Overview
Automated email notification system that alerts nurses about medicine inventory status via Gmail.

## 🎯 Features

### Automatic Email Alerts for:
1. **🚨 Expired Medicines** - Already expired, immediate action required
2. **⚠️ Expiring in 30 Days** - Urgent attention needed
3. **📅 Expiring in 60 Days** - Monitor closely
4. **📦 Low Stock** - 10 or fewer units remaining

### Consolidated Email Format
- **Single comprehensive email** with all alerts (not individual emails per medicine)
- Professional HTML email template with color-coded sections
- Summary dashboard showing total alerts by category
- Detailed tables for each alert type
- Sent to all nurses' email addresses in the system

## 📋 System Requirements

- Python 3.x installed
- Flask server running on http://127.0.0.1:5000
- Gmail SMTP access configured (already set up)
- Nurses must have valid email addresses in their user profiles

## 🚀 Setup Instructions

### Option 1: Automatic Daily Notifications (Recommended)

1. **Run the Setup Script as Administrator:**
   ```
   Right-click SETUP_DAILY_INVENTORY_NOTIFICATIONS.bat
   Select "Run as administrator"
   ```

2. **Verify Task Creation:**
   - Open Task Scheduler (Press Win+R, type `taskschd.msc`)
   - Look for task named: `iClinic_Daily_Inventory_Check`
   - Default schedule: Every day at 8:00 AM

3. **Customize Schedule (Optional):**
   - Open Task Scheduler
   - Find `iClinic_Daily_Inventory_Check`
   - Right-click → Properties → Triggers
   - Modify time/frequency as needed

### Option 2: Manual Testing

1. **Test the notification system:**
   ```bash
   python run_daily_inventory_check.py
   ```

2. **Or test via API (requires Flask server running):**
   - Login to iClinic as staff/nurse
   - Use API endpoint: `POST /api/inventory/send-notification`

## 📊 How It Works

### Daily Automated Check:
```
8:00 AM Daily → Windows Task Scheduler runs script
              → Script calls Flask API endpoint
              → System checks medicine_batches table
              → Identifies alerts based on criteria
              → Generates consolidated HTML email
              → Sends to all nurse email addresses
```

### Alert Criteria:

**Expired Medicines:**
- `expiry_date <= today`
- Shows days overdue

**Expiring in 30 Days:**
- `expiry_date <= today + 30 days`
- Shows days until expiry

**Expiring in 60 Days:**
- `expiry_date <= today + 60 days`
- Shows days until expiry

**Low Stock:**
- `total_quantity <= 10 units`
- Checks across all available batches

## 📧 Email Configuration

Current settings (already configured):
```python
SMTP Server: smtp.gmail.com
Port: 587
Email: norzagaraycollege.clinic@gmail.com
From Name: iClinic Inventory System
```

## 🔧 API Endpoints

### 1. Check Alerts (GET)
```
GET /api/inventory/check-alerts
```
Returns summary of current inventory alerts without sending email.

**Response:**
```json
{
  "success": true,
  "total_alerts": 5,
  "summary": {
    "expired": 1,
    "expiring_30_days": 2,
    "expiring_60_days": 1,
    "low_stock": 1
  }
}
```

### 2. Send Notification (POST)
```
POST /api/inventory/send-notification
```
Manually trigger email notification to all nurses.

**Requirements:**
- Must be logged in as staff
- Nurses must have email addresses in database

**Response:**
```json
{
  "success": true,
  "message": "Inventory notification sent to 2 nurse(s)",
  "recipients": ["nurse1@example.com", "nurse2@example.com"]
}
```

### 3. Scheduled Notification (POST)
```
POST /api/inventory/schedule-notification
```
Used by automated daily task. No authentication required.

## 📝 Email Template Preview

The email includes:

**Header:**
- 🏥 iClinic Inventory Alert
- Current date

**Summary Dashboard:**
- Total expired medicines
- Total expiring in 30 days
- Total expiring in 60 days
- Total low stock items

**Detailed Sections:**
1. **Expired Medicines Table**
   - Medicine name, batch number, quantity, expired date, days overdue, supplier

2. **Expiring in 30 Days Table**
   - Medicine name, batch number, quantity, expiry date, days until expiry, supplier

3. **Expiring in 60 Days Table**
   - Medicine name, batch number, quantity, expiry date, days until expiry, supplier

4. **Low Stock Table**
   - Medicine name, category, current stock, batch numbers

**Action Required Section:**
- Clear instructions on what actions to take
- Checklist for inventory management

## 🧪 Testing

### Test Notification Manually:

1. **Ensure Flask server is running:**
   ```bash
   python app.py
   ```

2. **Run test script:**
   ```bash
   python run_daily_inventory_check.py
   ```

3. **Check console output for:**
   - ✅ Connection successful
   - 📊 Alert summary
   - 📧 Email sent confirmation

4. **Check nurse email inbox** for notification

### Test Scheduled Task:

```bash
# Run task manually via Task Scheduler
schtasks /run /tn "iClinic_Daily_Inventory_Check"

# View task status
schtasks /query /tn "iClinic_Daily_Inventory_Check"

# View task history
# Open Task Scheduler → Find task → History tab
```

## 🔍 Troubleshooting

### No Email Received:

1. **Check nurse email addresses:**
   - Login to iClinic
   - Go to user management
   - Verify nurses have valid email addresses

2. **Check Flask server:**
   - Ensure server is running on port 5000
   - Check console for error messages

3. **Check email configuration:**
   - Verify Gmail credentials in app.py
   - Ensure Gmail App Password is valid
   - Check spam/junk folder

### Task Not Running:

1. **Verify task exists:**
   ```bash
   schtasks /query /tn "iClinic_Daily_Inventory_Check"
   ```

2. **Check task history:**
   - Open Task Scheduler
   - Find task → History tab
   - Look for errors

3. **Run manually to test:**
   ```bash
   schtasks /run /tn "iClinic_Daily_Inventory_Check"
   ```

### Script Errors:

1. **Check Python installation:**
   ```bash
   python --version
   ```

2. **Check required packages:**
   ```bash
   pip install flask mysql-connector-python requests
   ```

3. **Check database connection:**
   - Verify MySQL is running
   - Check database credentials in config/database.py

## 📅 Customizing Schedule

### Change notification time:

1. **Via Task Scheduler GUI:**
   - Open Task Scheduler
   - Find `iClinic_Daily_Inventory_Check`
   - Right-click → Properties → Triggers
   - Edit trigger → Change start time

2. **Via Command Line:**
   ```bash
   # Delete existing task
   schtasks /delete /tn "iClinic_Daily_Inventory_Check" /f
   
   # Create new task with different time (e.g., 9:00 AM)
   schtasks /create /tn "iClinic_Daily_Inventory_Check" /tr "python \"C:\xampp\htdocs\iClini V.2\run_daily_inventory_check.py\"" /sc daily /st 09:00 /f
   ```

### Change notification frequency:

**Multiple times per day:**
```bash
# Morning check (8:00 AM)
schtasks /create /tn "iClinic_Inventory_Morning" /tr "python \"C:\xampp\htdocs\iClini V.2\run_daily_inventory_check.py\"" /sc daily /st 08:00 /f

# Afternoon check (2:00 PM)
schtasks /create /tn "iClinic_Inventory_Afternoon" /tr "python \"C:\xampp\htdocs\iClini V.2\run_daily_inventory_check.py\"" /sc daily /st 14:00 /f
```

**Weekly instead of daily:**
```bash
# Every Monday at 8:00 AM
schtasks /create /tn "iClinic_Weekly_Inventory" /tr "python \"C:\xampp\htdocs\iClini V.2\run_daily_inventory_check.py\"" /sc weekly /d MON /st 08:00 /f
```

## 🎨 Customizing Email Content

Edit `services/inventory_notification_service.py`:

**Change alert thresholds:**
```python
# Line 30-32: Modify days
days_60 = today + timedelta(days=60)  # Change 60 to desired days
days_30 = today + timedelta(days=30)  # Change 30 to desired days

# Line 120: Modify low stock threshold
WHERE m.quantity_in_stock <= 10  # Change 10 to desired minimum
```

**Customize email styling:**
- Modify HTML in `create_email_html()` function
- Change colors, fonts, layout as needed

## 📞 Support

For issues or questions:
1. Check Flask server console for error messages
2. Review Task Scheduler history for task execution logs
3. Verify database connectivity
4. Check email configuration and credentials

## ✅ Success Indicators

When working correctly, you should see:
- ✅ Task appears in Task Scheduler
- ✅ Task runs daily at scheduled time
- ✅ Console shows successful execution
- ✅ Nurses receive consolidated email with all alerts
- ✅ Email contains accurate inventory data
- ✅ No error messages in Flask console

## 🔐 Security Notes

- Gmail App Password is stored in app.py (keep secure)
- Only staff users can manually trigger notifications
- Scheduled task runs without authentication (internal system)
- Email addresses are retrieved from database (not hardcoded)

# 📧 Sistema ng Email Notification para sa Inventory

## 🎯 Ano ang Ginagawa Nito?

Automatic email notification system na nag-sesend ng **CONSOLIDATED EMAIL** sa lahat ng nurses tungkol sa medicine inventory status.

### Nag-nonotify kapag:

1. **🚨 EXPIRED NA GAMOT** - Kailangan na alisin agad
2. **⚠️ 30 DAYS BAGO MAG-EXPIRE** - Urgent attention needed
3. **📅 60 DAYS BAGO MAG-EXPIRE** - Monitor closely
4. **📦 KONTI NA LANG GAMOT** - 10 or less units na lang

### ✨ Special Features:

- ✅ **ISANG EMAIL LANG** - Hindi isa-isa per gamot, consolidated lahat
- ✅ **LAHAT NG NURSES** - Sabay-sabay natatanggap ang email
- ✅ **PROFESSIONAL FORMAT** - May tables, colors, at clear information
- ✅ **AUTOMATIC DAILY** - Pwedeng i-schedule every morning
- ✅ **VIA GMAIL** - Gamit ang norzagaraycollege.clinic@gmail.com

## 🚀 Paano I-Setup (SIMPLE STEPS)

### Step 1: I-test Muna

```bash
# Siguraduhing running ang Flask server
python app.py

# Sa bagong terminal/command prompt, i-test ang system
python test_inventory_notification.py
```

Makikita mo:
- ✅ Database connection status
- 📊 Ilang alerts meron (expired, expiring, low stock)
- 📧 Ilang nurse emails nakita
- Option to send test email

### Step 2: I-setup ang Daily Automatic Email

**IMPORTANTE: Run as Administrator**

1. Right-click sa `SETUP_DAILY_INVENTORY_NOTIFICATIONS.bat`
2. Click "Run as administrator"
3. Tapos na! 🎉

Default schedule: **Every day at 8:00 AM**

### Step 3: I-verify ang Setup

1. Press `Win + R`
2. Type: `taskschd.msc`
3. Hanapin ang task: `iClinic_Daily_Inventory_Check`
4. Makikita mo doon ang schedule

## 📧 Ano ang Laman ng Email?

### Email Header:
```
🏥 iClinic Inventory Alert
Medicine Inventory Status Report - [Date]
```

### Summary Dashboard:
```
┌─────────────────────────────┐
│ 📊 Alert Summary            │
├─────────────────────────────┤
│ Expired Medicines:      2   │
│ Expiring in 30 Days:    3   │
│ Expiring in 60 Days:    1   │
│ Low Stock Items:        2   │
└─────────────────────────────┘
```

### Detailed Tables:

**1. EXPIRED MEDICINES** (Red Alert)
| Medicine Name | Batch Number | Quantity | Expired Date | Days Overdue | Supplier |
|--------------|--------------|----------|--------------|--------------|----------|
| Paracetamol  | BATCH-001    | 50 units | 2025-10-01   | 27 days      | ABC Pharma |

**2. EXPIRING IN 30 DAYS** (Orange Warning)
| Medicine Name | Batch Number | Quantity | Expiry Date  | Days Until Expiry | Supplier |
|--------------|--------------|----------|--------------|-------------------|----------|
| Amoxicillin  | BATCH-002    | 30 units | 2025-11-15   | 18 days           | XYZ Pharma |

**3. EXPIRING IN 60 DAYS** (Blue Info)
| Medicine Name | Batch Number | Quantity | Expiry Date  | Days Until Expiry | Supplier |
|--------------|--------------|----------|--------------|-------------------|----------|
| Ibuprofen    | BATCH-003    | 40 units | 2025-12-10   | 43 days           | ABC Pharma |

**4. LOW STOCK** (Yellow Warning)
| Medicine Name | Category | Current Stock | Batch Numbers |
|--------------|----------|---------------|---------------|
| Biogesic     | Analgesic| 8 units       | BATCH-004, BATCH-005 |

### Action Required Section:
- ✅ Remove expired medicines immediately
- ✅ Plan usage for expiring medicines
- ✅ Reorder low stock items
- ✅ Update inventory records

## 🔧 Paano Gamitin

### Option 1: Automatic (Recommended)

Kapag na-setup mo na ang Task Scheduler:
- **Walang gagawin** - Automatic na mag-sesend every 8:00 AM
- Basta running lang ang Flask server
- Check email ng nurses every morning

### Option 2: Manual Send

**Via Python Script:**
```bash
python run_daily_inventory_check.py
```

**Via API (kailangan naka-login as staff):**
```javascript
// Sa browser console o Postman
fetch('/api/inventory/send-notification', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
})
```

### Option 3: Check Alerts Only (Walang Email)

```javascript
// Para makita lang kung may alerts
fetch('/api/inventory/check-alerts')
```

## ⚙️ Paano I-customize

### Baguhin ang Schedule Time

**Via Task Scheduler:**
1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Find `iClinic_Daily_Inventory_Check`
3. Right-click → Properties → Triggers
4. Edit → Change time

**Via Command Line:**
```bash
# Delete old task
schtasks /delete /tn "iClinic_Daily_Inventory_Check" /f

# Create new task (example: 9:00 AM)
schtasks /create /tn "iClinic_Daily_Inventory_Check" /tr "python \"C:\xampp\htdocs\iClini V.2\run_daily_inventory_check.py\"" /sc daily /st 09:00 /f
```

### Baguhin ang Alert Thresholds

Edit `services/inventory_notification_service.py`:

```python
# Line 30-32: Days before expiry
days_60 = today + timedelta(days=60)  # Change 60 to 90 for 90 days
days_30 = today + timedelta(days=30)  # Change 30 to 15 for 15 days

# Line 120: Low stock threshold
WHERE m.quantity_in_stock <= 10  # Change 10 to 20 for 20 units minimum
```

### Multiple Times per Day

```bash
# Morning check (8:00 AM)
schtasks /create /tn "iClinic_Inventory_Morning" /tr "python \"C:\xampp\htdocs\iClini V.2\run_daily_inventory_check.py\"" /sc daily /st 08:00 /f

# Afternoon check (2:00 PM)
schtasks /create /tn "iClinic_Inventory_Afternoon" /tr "python \"C:\xampp\htdocs\iClini V.2\run_daily_inventory_check.py\"" /sc daily /st 14:00 /f
```

## 🧪 Testing

### Test 1: Check kung may alerts
```bash
python test_inventory_notification.py
```

### Test 2: Manual run ng scheduled task
```bash
schtasks /run /tn "iClinic_Daily_Inventory_Check"
```

### Test 3: Check task history
1. Open Task Scheduler
2. Find `iClinic_Daily_Inventory_Check`
3. Click "History" tab
4. Tignan kung successful ang last run

## 🔍 Troubleshooting

### Problem: Walang natatanggap na email

**Solution 1: Check nurse emails**
1. Login sa iClinic as admin
2. Check user management
3. Siguraduhing may valid email ang nurses

**Solution 2: Check Flask server**
```bash
# Siguraduhing running ang server
python app.py

# Check console for errors
```

**Solution 3: Check spam folder**
- Tingnan ang spam/junk folder ng email
- I-mark as "Not Spam" kung nandoon

### Problem: Task hindi tumatakbo

**Solution 1: Verify task exists**
```bash
schtasks /query /tn "iClinic_Daily_Inventory_Check"
```

**Solution 2: Run manually**
```bash
schtasks /run /tn "iClinic_Daily_Inventory_Check"
```

**Solution 3: Check permissions**
- Right-click bat file → Run as Administrator
- O kaya i-recreate ang task

### Problem: Python error

**Solution: Install required packages**
```bash
pip install flask mysql-connector-python requests
```

## 📊 Paano Makita ang Results

### Sa Console (Terminal):
```
========================================
🏥 iClinic Daily Inventory Check
📅 2025-10-28 08:00:00
========================================

📡 Connecting to iClinic server...

✅ Scheduled notification sent to 2 nurse(s)

📊 Alert Summary:
   Total Alerts: 8
   Recipients: nurse1@gmail.com, nurse2@gmail.com

📧 Email notification sent successfully!
========================================
```

### Sa Email:
- Check inbox ng nurses
- Subject: "🚨 iClinic Inventory Alert - 8 Items Need Attention"
- Professional HTML email with all details

### Sa Task Scheduler:
- Open Task Scheduler
- Find task → History tab
- Last Run Result: Success (0x0)

## 📝 Important Notes

1. **Flask Server Must Be Running**
   - Kailangan running ang `python app.py`
   - Para ma-access ang API endpoints

2. **Nurse Email Addresses**
   - Kailangan may email ang nurses sa database
   - Position = 'Nurse' sa users table

3. **Gmail Configuration**
   - Already configured sa app.py
   - Email: norzagaraycollege.clinic@gmail.com
   - Using Gmail App Password

4. **Consolidated Email**
   - Isang email lang per day
   - Lahat ng alerts nandoon
   - Hindi isa-isa per medicine

5. **Batch Tracking**
   - Uses medicine_batches table
   - Supports multiple batches per medicine
   - FIFO inventory management

## 🎯 Quick Start Checklist

- [ ] Test the system: `python test_inventory_notification.py`
- [ ] Setup daily task: Run `SETUP_DAILY_INVENTORY_NOTIFICATIONS.bat` as Admin
- [ ] Verify task in Task Scheduler
- [ ] Check nurse email addresses in database
- [ ] Test manual run: `python run_daily_inventory_check.py`
- [ ] Wait for scheduled time or run task manually
- [ ] Check nurse email inbox
- [ ] Verify email received with correct data

## 📞 Need Help?

1. Read `INVENTORY_NOTIFICATION_GUIDE.md` for detailed documentation
2. Check Flask console for error messages
3. Review Task Scheduler history
4. Test with `test_inventory_notification.py`
5. Verify database connection and nurse emails

## ✅ Success Indicators

Kapag gumagana ng maayos:
- ✅ Task visible sa Task Scheduler
- ✅ Task runs daily at scheduled time
- ✅ Console shows "✅ Email notification sent successfully"
- ✅ Nurses receive consolidated email
- ✅ Email contains accurate inventory data
- ✅ No errors sa Flask console

---

**Created by:** iClinic Development Team  
**Version:** 1.0  
**Last Updated:** October 2025

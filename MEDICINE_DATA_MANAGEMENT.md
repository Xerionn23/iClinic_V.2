# Medicine Data Management Guide

## ❌ PROBLEMA: Data ay bumabalik pagkatapos i-delete

### Root Cause
Ang iClinic system ay **WALANG automatic sample data insertion** para sa medicines table. Kung bumabalik ang data pagkatapos i-delete, may dalawang possible reasons:

1. **Hindi na-delete sa tamang table** - Ang system ay gumagamit ng `medicines` table, hindi `medicine_inventory`
2. **May cached data sa browser** - Ang frontend ay nag-cache ng data
3. **Hindi nag-commit ang database transaction** - Ang DELETE query ay hindi nag-save

---

## ✅ TAMANG PARAAN NG PAG-DELETE NG MEDICINES

### Option 1: Delete via Staff-Inventory Interface
1. Login as staff sa system
2. Go to **Staff-Inventory.html**
3. Click ang **Delete button** (trash icon) sa medicine na gusto mong i-delete
4. Confirm ang deletion
5. **IMPORTANTE**: Refresh ang page (F5) para ma-verify na wala na talaga

### Option 2: Delete Directly sa Database (phpMyAdmin)
1. Open **phpMyAdmin** (http://localhost/phpmyadmin)
2. Select database: **`iclinic_db`**
3. Click ang **`medicines`** table (HINDI `medicine_inventory`)
4. Select ang rows na gusto mong i-delete
5. Click **"Delete"** button
6. Confirm ang deletion
7. **IMPORTANTE**: Clear browser cache at i-refresh ang page

### Option 3: Delete All Medicines (Complete Reset)
```sql
-- Run this sa phpMyAdmin SQL tab
TRUNCATE TABLE medicine_batches;  -- Delete batches first (foreign key)
TRUNCATE TABLE medicines;          -- Then delete medicines
```

---

## 🔍 PAANO I-VERIFY NA WALA NANG DATA

### 1. Check sa Database
```sql
-- Run this sa phpMyAdmin
SELECT COUNT(*) FROM medicines;
-- Result dapat: 0
```

### 2. Check sa System
1. Go to Staff-Inventory page
2. Refresh ang page (Ctrl+Shift+R para hard refresh)
3. Dapat walang medicines sa table
4. Statistics cards dapat lahat 0

### 3. Clear Browser Cache
```
Chrome/Edge: Ctrl+Shift+Delete → Clear cached images and files
Firefox: Ctrl+Shift+Delete → Cached Web Content
```

---

## 📊 DATABASE TABLES STRUCTURE

### `medicines` Table (Main Table)
- `medicine_id` - Primary key
- `medicine_name` - Name ng medicine
- `brand_name` - Brand name
- `generic_name` - Generic name
- `category` - Category (Antibiotic, Pain Reliever, etc.)
- `dosage_form` - Form (Tablet, Capsule, Syrup, etc.)
- `strength` - Strength (500mg, 250mg, etc.)
- `quantity_in_stock` - Total quantity
- `price` - Price per unit
- `expiry_date` - Expiration date
- `status` - Status (Available, Low Stock, Expired, etc.)
- `date_added` - Date added to inventory

### `medicine_batches` Table (Batch Tracking)
- `id` - Primary key
- `medicine_id` - Foreign key to medicines table
- `batch_number` - Batch/Lot number
- `quantity` - Quantity sa batch na ito
- `expiry_date` - Expiry date ng batch
- `arrival_date` - Date ng arrival
- `supplier` - Supplier name
- `cost_per_unit` - Cost per unit
- `notes` - Additional notes
- `status` - Status ng batch

---

## 🚫 WALANG AUTOMATIC SAMPLE DATA INSERTION

Ang init_db() function sa app.py ay:
- ✅ Nag-create ng `medicines` table kung wala pa
- ✅ Nag-create ng `medicine_batches` table kung wala pa
- ❌ **HINDI nag-insert ng sample medicines data**
- ❌ **HINDI nag-auto-populate ng data**

Ang sample data insertion ay **MANUAL LANG** through:
- `/api/create-expired-test-data` endpoint (manual trigger)
- Staff-Inventory interface (manual add)
- Direct database insertion (manual SQL)

---

## 🔧 TROUBLESHOOTING

### Problema: Data ay bumabalik pa rin pagkatapos i-delete

**Solution 1: Hard Refresh**
```
Windows: Ctrl+Shift+R o Ctrl+F5
Mac: Cmd+Shift+R
```

**Solution 2: Clear Browser Cache**
1. Open DevTools (F12)
2. Right-click sa Refresh button
3. Select "Empty Cache and Hard Reload"

**Solution 3: Check Database Directly**
```sql
-- Verify na wala nang data
SELECT * FROM medicines;
SELECT * FROM medicine_batches;
```

**Solution 4: Restart Flask Server**
```bash
# Stop ang server (Ctrl+C)
# Then run again:
python app.py
```

### Problema: Hindi ma-delete ang medicine

**Possible Causes:**
1. **Foreign Key Constraint** - May batches pa sa medicine_batches table
   ```sql
   -- Delete batches first
   DELETE FROM medicine_batches WHERE medicine_id = [ID];
   -- Then delete medicine
   DELETE FROM medicines WHERE medicine_id = [ID];
   ```

2. **Session/Permission Issue** - Hindi naka-login as staff
   - Solution: Logout then login again

3. **Database Lock** - May ongoing transaction
   - Solution: Restart MySQL service sa XAMPP

---

## 📝 BEST PRACTICES

1. **Always use the Staff-Inventory interface** para sa delete operations
2. **Verify deletion** by refreshing the page
3. **Clear browser cache** kung may caching issues
4. **Backup database** before bulk deletions
5. **Use batch tracking** para sa proper FIFO inventory management

---

## 🎯 SUMMARY

- ✅ System ay **WALANG auto-insert** ng sample medicines data
- ✅ `medicines` table ay properly created sa init_db()
- ✅ Delete operations ay working through API endpoints
- ✅ Data persistence ay handled ng MySQL database
- ❌ Kung bumabalik ang data, check browser cache o database directly

**Kung may problema pa rin, i-check ang:**
1. Browser cache
2. Database table (`medicines` not `medicine_inventory`)
3. MySQL transaction commit
4. Flask server restart

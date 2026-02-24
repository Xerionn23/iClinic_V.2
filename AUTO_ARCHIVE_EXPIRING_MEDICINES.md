# 🗄️ Auto-Archive Expiring Medicines

## ✅ **IMPLEMENTED: Automatic Archive for Medicines Expiring Within 30 Days**

Ang medicines na **30 days or less before expiration** ay automatic na:
- ❌ **Mawawala sa Medicines table**
- ✅ **Lalabas sa Archive tab**

---

## 🎯 **HOW IT WORKS:**

### **Rule:**
```
If medicine expiry date <= 30 days from today:
    → Remove from Medicines table
    → Show in Archive (Expired Medicines)
```

### **Examples:**

**Today: 2025-10-18**

| Medicine | Expiry Date | Days Left | Location |
|----------|-------------|-----------|----------|
| Paracetamol | 2025-12-31 | 74 days | ✅ Medicines Table |
| Amoxicillin | 2025-11-15 | 28 days | 🗄️ Archive (Expiring Soon) |
| Biogesic | 2025-10-10 | -8 days | 🗄️ Archive (Expired) |
| Ibuprofen | 2025-11-17 | 30 days | 🗄️ Archive (Exactly 30 days) |

---

## 🔧 **TECHNICAL IMPLEMENTATION:**

### **1. Updated `filteredMedicines` Computed Property**

**Before:**
```javascript
get filteredMedicines() {
    return this.medicines.filter(medicine => {
        // Only search, category, status filters
        return matchesSearch && matchesCategory && matchesStatus;
    });
}
```

**After:**
```javascript
get filteredMedicines() {
    return this.medicines.filter(medicine => {
        // Calculate days until expiry
        const daysUntilExpiry = this.getDaysUntilExpiry(medicine.expiry_date);
        const isExpiringSoonOrExpired = daysUntilExpiry <= 30;
        
        // Exclude medicines expiring within 30 days or already expired
        if (isExpiringSoonOrExpired) {
            return false; // ← HIDE from Medicines table
        }
        
        // Continue with other filters
        return matchesSearch && matchesCategory && matchesStatus;
    });
}
```

---

### **2. Updated `expiredMedicines` Computed Property**

**Before:**
```javascript
get expiredMedicines() {
    // Only show expired medicines (past expiry date)
    return this.medicines.filter(medicine => {
        const expiryDate = new Date(medicine.expiry_date);
        return expiryDate < today;
    });
}
```

**After:**
```javascript
get expiredMedicines() {
    return this.medicines.filter(medicine => {
        const daysUntilExpiry = this.getDaysUntilExpiry(medicine.expiry_date);
        
        // Include medicines that are:
        // 1. Already expired (daysUntilExpiry < 0)
        // 2. Expiring within 30 days (daysUntilExpiry <= 30)
        const isExpiredOrExpiringSoon = daysUntilExpiry <= 30;
        
        return isExpiredOrExpiringSoon; // ← SHOW in Archive
    });
}
```

---

## 📊 **VISUAL FLOW:**

### **Medicines Table (Active Inventory):**
```
┌─────────────────────────────────────────┐
│ MEDICINES (Active Inventory)           │
├─────────────────────────────────────────┤
│ ✅ Paracetamol    | Exp: 2025-12-31    │ ← 74 days left
│ ✅ Cetirizine     | Exp: 2026-01-15    │ ← 89 days left
│ ✅ Mefenamic Acid | Exp: 2025-11-30    │ ← 43 days left
└─────────────────────────────────────────┘
```

### **Archive Tab (Expired/Expiring):**
```
┌─────────────────────────────────────────┐
│ ARCHIVE (Expired & Expiring Soon)      │
├─────────────────────────────────────────┤
│ ⚠️ Amoxicillin    | Exp: 2025-11-15    │ ← 28 days left
│ ⚠️ Ibuprofen      | Exp: 2025-11-17    │ ← 30 days left
│ ❌ Biogesic       | Exp: 2025-10-10    │ ← Expired (8 days ago)
│ ❌ Aspirin        | Exp: 2025-09-30    │ ← Expired (18 days ago)
└─────────────────────────────────────────┘
```

---

## 🔍 **CONSOLE LOGS:**

### **When Loading Medicines:**
```
🗄️ Checking expired/expiring medicines...
📅 Today: 2025-10-18
📦 Total medicines to check: 10

  ⚠️ EXPIRING SOON: Amoxicillin - Expiry: 2025-11-15 (28 days left)
  ⚠️ EXPIRING SOON: Ibuprofen - Expiry: 2025-11-17 (30 days left)
  ❌ EXPIRED: Biogesic - Expiry: 2025-10-10 (8 days ago)
  ❌ EXPIRED: Aspirin - Expiry: 2025-09-30 (18 days ago)

🗄️ Total expired/expiring medicines: 4
```

---

## 📋 **ARCHIVE TAB DISPLAY:**

### **Status Indicators:**

**Expired (Past Date):**
```html
<span class="bg-red-100 text-red-800">
    ❌ EXPIRED (8 days ago)
</span>
```

**Expiring Soon (Within 30 days):**
```html
<span class="bg-orange-100 text-orange-800">
    ⚠️ EXPIRING SOON (28 days left)
</span>
```

---

## ✅ **VERIFICATION STEPS:**

### **Test Scenario 1: Medicine Expiring in 25 Days**

1. **Add medicine:**
   - Name: Test Medicine
   - Expiry Date: 2025-11-12 (25 days from 2025-10-18)

2. **Expected Result:**
   - ❌ NOT visible in Medicines table
   - ✅ Visible in Archive tab
   - Label: "⚠️ EXPIRING SOON (25 days left)"

### **Test Scenario 2: Medicine Expiring in 35 Days**

1. **Add medicine:**
   - Name: Test Medicine 2
   - Expiry Date: 2025-11-22 (35 days from 2025-10-18)

2. **Expected Result:**
   - ✅ Visible in Medicines table
   - ❌ NOT in Archive tab

### **Test Scenario 3: Expired Medicine**

1. **Add medicine:**
   - Name: Test Medicine 3
   - Expiry Date: 2025-10-10 (8 days ago)

2. **Expected Result:**
   - ❌ NOT visible in Medicines table
   - ✅ Visible in Archive tab
   - Label: "❌ EXPIRED (8 days ago)"

---

## 🎨 **USER EXPERIENCE:**

### **Medicines Tab:**
- Shows only **active medicines** (more than 30 days before expiry)
- Clean, focused inventory
- No expired or soon-to-expire items cluttering the view

### **Archive Tab:**
- Shows **expired medicines** (past expiry date)
- Shows **expiring soon** (30 days or less)
- Clear visual indicators (red for expired, orange for expiring soon)
- Days remaining/past displayed

---

## 📊 **STATISTICS UPDATE:**

### **Medicines Tab Statistics:**
```
Total Medicines: 6        ← Only active medicines
Low Stock: 2
Expiring Soon: 0          ← None shown here
Categories: 4
```

### **Archive Tab Statistics:**
```
Total Expired Items: 4    ← Expired + Expiring Soon
Expired Medicines: 4
Expired Supplies: 0
Items to Dispose: 4
```

---

## 🔄 **AUTOMATIC BEHAVIOR:**

### **Daily Automatic Movement:**

**Day 1 (31 days before expiry):**
- Medicine: ✅ In Medicines table

**Day 2 (30 days before expiry):**
- Medicine: 🗄️ Moved to Archive automatically

**Day 32 (Expired):**
- Medicine: 🗄️ Still in Archive

**No manual action needed!** The system automatically filters based on current date.

---

## ⚠️ **IMPORTANT NOTES:**

### **30-Day Threshold:**
- Medicines with **exactly 30 days** left → Archive
- Medicines with **31 days** left → Medicines table
- Medicines with **29 days** left → Archive

### **No Database Changes:**
- Medicines are NOT deleted from database
- Only **display filtering** changes
- Data remains intact for records

### **Batch-Level Expiry:**
- If medicine has multiple batches
- System uses **earliest expiry date** from batches
- If earliest batch expires in 30 days → Entire medicine moves to Archive

---

## 🎉 **SUMMARY:**

### **What Changed:**
- ✅ Medicines expiring ≤ 30 days → Auto-hide from Medicines table
- ✅ Medicines expiring ≤ 30 days → Auto-show in Archive
- ✅ Console logs show expiry status
- ✅ Visual indicators (⚠️ expiring, ❌ expired)

### **Benefits:**
- ✅ Clean active inventory (no expired items)
- ✅ Easy identification of items to dispose
- ✅ Automatic daily updates (no manual sorting)
- ✅ Better inventory management
- ✅ Compliance with pharmacy standards

**Ngayon, automatic na ang pag-move ng medicines sa Archive kapag 30 days or less na lang before expiration!** 🗄️✅

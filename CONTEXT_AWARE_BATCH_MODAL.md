# 🎯 Context-Aware Batch Modal

## ✅ **IMPLEMENTED: Filtered Batch Display Based on Tab Context**

Ang batch modal ay ngayon **context-aware** - nag-show lang ng relevant batches depende sa kung saan mo siya binuksan!

---

## 🔄 **HOW IT WORKS:**

### **Medicines Tab → View Batches:**
```
Shows: ACTIVE BATCHES ONLY (>30 days before expiry)
Hides: Expired/Expiring batches (≤30 days)
```

### **Archive Tab → View Batches:**
```
Shows: EXPIRED/EXPIRING BATCHES ONLY (≤30 days)
Hides: Active batches (>30 days)
```

---

## 📊 **EXAMPLE: Amoxicilline**

### **Medicine Data:**
```
Amoxicilline (Jeniebeth)
├── Batch 1: 23 units, Expires: 2025-10-30 (12 days) ⚠️
└── Batch 2: 50 units, Expires: 2026-07-31 (286 days) ✅
```

### **From Medicines Tab:**
```
Click "View Batches" button
    ↓
Modal shows:
┌─────────────────────────────────────────┐
│ 📦 Medicine Batches                     │
│ Amoxicilline (Jeniebeth)                │
├─────────────────────────────────────────┤
│ Batch #  │ Qty  │ Expiry      │ Status  │
├─────────────────────────────────────────┤
│ N/A      │ 50   │ 2026-07-31  │ ✅      │
└─────────────────────────────────────────┘
Active Batches: 1
Total Quantity: 73 units
```

**Result:** Only Batch 2 (active) is shown! ✅

---

### **From Archive Tab:**
```
Click "View Batches" button
    ↓
Modal shows:
┌─────────────────────────────────────────┐
│ 📦 Medicine Batches                     │
│ Amoxicilline (Jeniebeth)                │
├─────────────────────────────────────────┤
│ Batch #  │ Qty  │ Expiry      │ Status  │
├─────────────────────────────────────────┤
│ N/A      │ 23   │ 2025-10-30  │ ⚠️      │
│          │      │ [Expiring Soon]        │
└─────────────────────────────────────────┘
Expiring Batches: 1
Total Quantity: 73 units
```

**Result:** Only Batch 1 (expiring) is shown! ✅

---

## 🔧 **TECHNICAL IMPLEMENTATION:**

### **1. Added Context State:**
```javascript
batchesViewContext: 'all', // 'all', 'active', 'expired'
```

### **2. Updated viewBatches Function:**
```javascript
viewBatches(medicine, context = 'all') {
    this.selectedMedicineForBatches = medicine;
    this.batchesViewContext = context;
    this.showBatchesModal = true;
    console.log(`📦 Viewing batches for ${medicine.name} - Context: ${context}`);
}
```

### **3. Added Computed Property for Filtering:**
```javascript
get filteredBatchesForModal() {
    if (!this.selectedMedicineForBatches || !this.selectedMedicineForBatches.batches) {
        return [];
    }
    
    const batches = this.selectedMedicineForBatches.batches;
    
    if (this.batchesViewContext === 'active') {
        // Show only batches with > 30 days
        return batches.filter(batch => {
            const daysUntilExpiry = this.getDaysUntilExpiry(batch.expiry_date);
            return daysUntilExpiry > 30;
        });
    } else if (this.batchesViewContext === 'expired') {
        // Show only batches with <= 30 days
        return batches.filter(batch => {
            const daysUntilExpiry = this.getDaysUntilExpiry(batch.expiry_date);
            return daysUntilExpiry <= 30;
        });
    }
    
    // Show all batches
    return batches;
}
```

### **4. Updated Button Clicks:**

**Medicines Tab:**
```html
<button @click="viewBatches(medicine, 'active')" 
        title="View Active Batches">
    <i data-feather="package"></i>
</button>
```

**Archive Tab:**
```html
<button @click="viewBatches(medicine, 'expired')" 
        title="View Expired/Expiring Batches">
    <i data-feather="package"></i>
</button>
```

### **5. Updated Modal Display:**
```html
<!-- Use filtered batches -->
<template x-for="(batch, index) in filteredBatchesForModal" :key="batch.id">
    <tr>
        <td x-text="batch.batch_number"></td>
        <td x-text="batch.quantity"></td>
        <td x-text="batch.expiry_date"></td>
        ...
    </tr>
</template>
```

### **6. Context-Aware Empty State:**
```html
<div x-show="filteredBatchesForModal.length === 0">
    <span x-show="batchesViewContext === 'active'">
        No active batches found (all batches are expiring soon).
    </span>
    <span x-show="batchesViewContext === 'expired'">
        No expired/expiring batches found.
    </span>
    <span x-show="batchesViewContext === 'all'">
        No batches found for this medicine.
    </span>
</div>
```

### **7. Context-Aware Summary:**
```html
<div class="text-xs text-gray-500 uppercase">
    <span x-show="batchesViewContext === 'active'">Active Batches</span>
    <span x-show="batchesViewContext === 'expired'">Expiring Batches</span>
    <span x-show="batchesViewContext === 'all'">Total Batches</span>
</div>
<div class="text-lg font-semibold" x-text="filteredBatchesForModal.length"></div>
```

---

## 🔍 **CONSOLE LOGS:**

### **From Medicines Tab:**
```
📦 Viewing batches for Amoxicilline - Context: active
```

### **From Archive Tab:**
```
📦 Viewing batches for Amoxicilline - Context: expired
```

---

## 📋 **USER EXPERIENCE:**

### **Scenario 1: View from Medicines Tab**

**User Action:**
1. Go to **Medicines** tab
2. Find "Amoxicilline"
3. Click **View Batches** button (package icon)

**Expected Result:**
- Modal opens
- Title: "📦 Medicine Batches - Amoxicilline (Jeniebeth)"
- Shows: **1 batch** (Batch 2: 50 units, 2026-07-31)
- Hides: Batch 1 (expiring in 12 days)
- Summary: "Active Batches: 1"

**Why:** User is in Medicines tab, so they only want to see **usable/active batches**

---

### **Scenario 2: View from Archive Tab**

**User Action:**
1. Go to **Archive** tab
2. Find "Amoxicilline"
3. Click **View Batches** button (package icon)

**Expected Result:**
- Modal opens
- Title: "📦 Medicine Batches - Amoxicilline (Jeniebeth)"
- Shows: **1 batch** (Batch 1: 23 units, 2025-10-30 [Expiring Soon])
- Hides: Batch 2 (active batch with 286 days)
- Summary: "Expiring Batches: 1"

**Why:** User is in Archive tab, so they only want to see **expired/expiring batches** that need attention

---

## 🎯 **BENEFITS:**

### **1. Context-Aware Display:**
- ✅ Medicines tab → Shows only active batches
- ✅ Archive tab → Shows only expiring batches
- ✅ No confusion about which batches are relevant

### **2. Clear Information:**
- ✅ Users see only what matters in current context
- ✅ No need to mentally filter batches
- ✅ Easier to identify what to use/dispose

### **3. Better UX:**
- ✅ Focused information display
- ✅ Context-aware labels ("Active Batches" vs "Expiring Batches")
- ✅ Appropriate empty states

---

## ✅ **VERIFICATION:**

### **Test Case 1: Amoxicilline from Medicines Tab**

**Steps:**
1. Go to Medicines tab
2. Find Amoxicilline
3. Click View Batches

**Expected:**
- Shows 1 batch (50 units, 2026-07-31)
- Summary: "Active Batches: 1"
- Console: `📦 Viewing batches for Amoxicilline - Context: active`

---

### **Test Case 2: Amoxicilline from Archive Tab**

**Steps:**
1. Go to Archive tab
2. Find Amoxicilline
3. Click View Batches

**Expected:**
- Shows 1 batch (23 units, 2025-10-30 [Expiring Soon])
- Summary: "Expiring Batches: 1"
- Console: `📦 Viewing batches for Amoxicilline - Context: expired`

---

### **Test Case 3: Medicine with All Active Batches**

**Medicine:** Paracetamol (all batches expire >30 days)

**From Medicines Tab:**
- Shows all batches ✅

**From Archive Tab:**
- Should NOT appear in Archive ❌
- (Because no expiring batches)

---

### **Test Case 4: Medicine with All Expiring Batches**

**Medicine:** Biogesic (all batches expire ≤30 days)

**From Medicines Tab:**
- Should NOT appear in Medicines ❌
- (Because no active batches)

**From Archive Tab:**
- Shows all batches ✅

---

## 🎉 **SUMMARY:**

### **Before:**
- ❌ Modal always showed ALL batches
- ❌ User had to manually identify which are active/expiring
- ❌ Confusing when viewing from different tabs

### **After:**
- ✅ Modal shows FILTERED batches based on context
- ✅ Medicines tab → Active batches only
- ✅ Archive tab → Expiring batches only
- ✅ Clear, focused information display

**Ngayon, pag nag-click ka ng "View Batches" sa Medicines tab, active batches lang ang lalabas! Pag sa Archive tab naman, expiring batches lang!** 🎯✅

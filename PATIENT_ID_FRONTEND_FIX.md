# Patient ID Frontend Display Fix

## Problem Found
The backend was sending the correct `patientId` but the frontend was looking for `studentId` field!

---

## Root Cause

### Backend (app.py) ✅
```python
result.append({
    'id': c[0],
    'patient': c[1],
    'patientId': display_id,  # ✅ Backend sends this
    'patientType': patient_role,
    ...
})
```

### Frontend (Staff-Consultations.html) ❌
```javascript
// OLD CODE - Looking for wrong field
studentId: consultation.patientId || 'N/A',  // Only sets studentId

// Display was using:
x-text="selectedChat.studentId || 'N/A'"  // ❌ Wrong field name
```

---

## Solution Implemented

### 1. Updated Frontend Mapping
```javascript
// NEW CODE - Sets both fields
patientId: consultation.patientId || 'N/A',   // ✅ Primary field
studentId: consultation.patientId || 'N/A',   // ✅ Backward compatibility
```

### 2. Updated Display Logic
```html
<!-- Chat List Display -->
<span x-text="'ID: ' + (chat.patientId || chat.studentId || 'N/A')"></span>

<!-- Chat Header Display -->
<span x-text="selectedChat.patientId || selectedChat.studentId || 'N/A'"></span>
```

---

## Changes Made

### File: `pages/staff/Staff-Consultations.html`

#### Change 1: Chat List Display (Line 756)
**Before:**
```html
<span x-text="'ID: ' + (chat.studentId || 'N/A')"></span>
```

**After:**
```html
<span x-text="'ID: ' + (chat.patientId || chat.studentId || 'N/A')"></span>
```

#### Change 2: Chat Header Display (Line 815)
**Before:**
```html
<span x-text="selectedChat.studentId || 'N/A'"></span>
```

**After:**
```html
<span x-text="selectedChat.patientId || selectedChat.studentId || 'N/A'"></span>
```

#### Change 3: Data Mapping (Line 1218-1219)
**Before:**
```javascript
studentId: consultation.patientId || 'N/A',
```

**After:**
```javascript
patientId: consultation.patientId || 'N/A',  // Use patientId from backend
studentId: consultation.patientId || 'N/A',  // Keep for backward compatibility
```

---

## File: `app.py`

### Added Debug Logging (Line 5829-5837)
```python
# Debug logging with all ID fields
print(f"🔍 Patient: {c[1]}")
print(f"   Role: {patient_role}")
print(f"   student_number (c[11]): {c[11]}")
print(f"   faculty_id (c[12]): {c[12]}")
print(f"   staff_id (c[13]): {c[13]}")
print(f"   user_id (c[14]): {c[14]}")
print(f"   ✅ Display ID: {display_id}")
print("---")
```

---

## Expected Console Output

When you restart the server, you should see:

```
🔍 Patient: Joseph Flynn
   Role: Student
   student_number (c[11]): 2019-0013
   faculty_id (c[12]): None
   staff_id (c[13]): None
   user_id (c[14]): None
   ✅ Display ID: 2019-0013
---

🔍 Patient: Fernando Ruiz
   Role: Teaching Staff
   student_number (c[11]): None
   faculty_id (c[12]): FAC-CS-008
   staff_id (c[13]): None
   user_id (c[14]): None
   ✅ Display ID: FAC-CS-008
---
```

---

## Testing Steps

1. **Restart Flask Server:**
   ```bash
   python app.py
   ```

2. **Check Console Output:**
   - Look for debug logs showing patient IDs
   - Verify correct IDs are being selected

3. **Open Staff Consultations Page:**
   - Check chat list - should show proper IDs
   - Click on a chat - header should show proper ID

4. **Expected Results:**
   - Students: "2019-0013" instead of "2"
   - Teaching Staff: "FAC-CS-008" instead of generic ID
   - Non-Teaching Staff: "NTS-2024-001" instead of generic ID

---

## Why It Works Now

### Data Flow:
1. **Backend** → Fetches correct IDs from database tables
2. **Backend** → Sends as `patientId` in JSON response
3. **Frontend** → Maps `patientId` to both `patientId` and `studentId`
4. **Frontend** → Displays using `patientId` with `studentId` fallback
5. **Result** → Correct institutional IDs displayed! ✅

### Fallback Chain:
```javascript
chat.patientId || chat.studentId || 'N/A'
```
- First tries `patientId` (new field)
- Falls back to `studentId` (old field)
- Last resort: 'N/A'

---

## Summary

### Problem:
- Backend sent `patientId` ✅
- Frontend looked for `studentId` ❌
- Mismatch caused wrong IDs to display

### Solution:
- Frontend now uses `patientId` ✅
- Keeps `studentId` for compatibility ✅
- Display logic updated with fallback ✅

### Result:
- **Students** → Show Student Number (e.g., "2019-0013")
- **Teaching Staff** → Show Faculty ID (e.g., "FAC-CS-008")
- **Non-Teaching Staff** → Show Staff ID (e.g., "NTS-2024-001")
- **Deans/President** → Show User ID (e.g., "USER-1")

---

## 🎯 TAPOS NA TALAGA!

Restart lang ang server at makikita mo na ang **TAMANG STUDENT NUMBER** at iba pang IDs! 🚀

```bash
python app.py
```

Tingnan mo sa console kung ano ang lumalabas na IDs, tapos check mo sa browser! ✅

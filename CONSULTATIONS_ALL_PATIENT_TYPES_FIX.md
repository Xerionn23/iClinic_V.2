# Consultations - All Patient Types Support

## Problem Identified
The consultations table was only showing **Students** from the `medical_records` table. When staff added medical records for:
- 🏛️ **Visitors** (Presidents, Deans, Walk-ins)
- 👨‍🏫 **Teaching Staff**
- 👨‍💼 **Non-Teaching Staff**

These records were NOT appearing in the consultations list because the API only queried the `medical_records` table.

## Root Cause
The `/api/test-all-medical-records` endpoint was only querying:
```sql
SELECT * FROM medical_records mr
LEFT JOIN students s ON mr.student_number = s.student_number
```

This ignored the `visitor_medical_records` table where all non-student medical records are stored.

## Solution Implemented

### 1. UNION Query for Multiple Patient Types
Updated the SQL query to combine records from BOTH tables:

```sql
-- Student medical records
SELECT 
    mr.id, mr.student_number as patient_id, mr.visit_date, mr.visit_time, mr.chief_complaint,
    -- ... all medical fields ...
    CONCAT(s.std_Firstname, ' ', s.std_Surname) as patient_name,
    'Student' as patient_role,
    s.std_Course as additional_info
FROM medical_records mr
LEFT JOIN students s ON mr.student_number = s.student_number

UNION ALL

-- Visitor medical records (includes Presidents, Deans, Teaching Staff, Non-Teaching Staff, Walk-ins)
SELECT 
    vmr.id, vmr.visitor_id as patient_id, vmr.visit_date, vmr.visit_time, vmr.chief_complaint,
    -- ... all medical fields ...
    v.full_name as patient_name,
    'Visitor' as patient_role,
    v.purpose_of_visit as additional_info
FROM visitor_medical_records vmr
LEFT JOIN visitors v ON vmr.visitor_id = v.id

ORDER BY visit_date DESC, visit_time DESC
```

### 2. Simplified Data Processing
Since patient name and role are now computed in SQL, the backend processing is much simpler:

```python
# Get patient name and role from UNION query
patient_name = r[29] if r[29] and str(r[29]).strip() else f"Patient {r[1]}"
patient_role = r[30] if r[30] else 'Student'
additional_info = r[31] if r[31] else ''
```

### 3. Patient Role Detection
The system now automatically identifies patient types:

| Patient Type | Source Table | Role Field | Additional Info |
|-------------|--------------|------------|-----------------|
| **Students** | `medical_records` | "Student" | Course (e.g., "BSIT") |
| **Visitors** | `visitor_medical_records` | "Visitor" | Purpose (e.g., "President Visit") |
| **Teaching Staff** | `visitor_medical_records` | "Visitor" | Purpose (e.g., "Faculty Checkup") |
| **Non-Teaching Staff** | `visitor_medical_records` | "Visitor" | Purpose (e.g., "Staff Consultation") |

**Note**: Currently, all non-students are categorized as "Visitor" in the database. To distinguish between actual visitors, teaching staff, and non-teaching staff, we would need to:
1. Add a `patient_type` column to the `visitors` table, OR
2. Create separate tables for each staff type, OR
3. Use the `purpose_of_visit` field to infer the type

## Color-Coded Display

The frontend now shows proper role badges:

- 🔵 **Student** - Blue badge - From `medical_records` table
- 🟠 **Visitor** - Orange badge - From `visitor_medical_records` table
  - Includes: Presidents, Deans, Teaching Staff, Non-Teaching Staff, Walk-ins

## Database Tables Used

### medical_records (Students Only)
- Linked to `students` table via `student_number`
- Contains: Student medical history, consultations, treatments
- Role: Always "Student"

### visitor_medical_records (All Non-Students)
- Linked to `visitors` table via `visitor_id`
- Contains: Visitor medical history, consultations, treatments
- Role: "Visitor" (includes all non-student types)
- Purpose field indicates: President, Dean, Teaching Staff, Non-Teaching Staff, Walk-in

## Result

✅ **Students** - Show in consultations table with blue "Student" badge
✅ **Visitors** - Show in consultations table with orange "Visitor" badge
✅ **Presidents/Deans** - Show in consultations table with orange "Visitor" badge
✅ **Teaching Staff** - Show in consultations table with orange "Visitor" badge
✅ **Non-Teaching Staff** - Show in consultations table with orange "Visitor" badge

## Example Records

After the fix, the consultations table will show:

| Patient Name | Role | Chief Complaint | Date |
|-------------|------|-----------------|------|
| Juan Dela Cruz | 🔵 Student | Headache | Oct 17, 2025 |
| Dr. Maria Santos | 🟠 Visitor | Annual Checkup | Oct 16, 2025 |
| President Jose Garcia | 🟠 Visitor | Blood Pressure Monitoring | Oct 15, 2025 |
| Ana Rodriguez | 🔵 Student | Fever | Oct 14, 2025 |

## Future Enhancement: Separate Staff Roles

To show Teaching Staff and Non-Teaching Staff with their own badges, we can:

### Option 1: Add patient_type column to visitors table
```sql
ALTER TABLE visitors ADD COLUMN patient_type VARCHAR(50) DEFAULT 'Visitor';
-- Values: 'Visitor', 'Teaching Staff', 'Non-Teaching Staff', 'President', 'Dean'
```

### Option 2: Infer from purpose_of_visit
```python
# In backend processing
if 'teaching' in purpose.lower() or 'faculty' in purpose.lower():
    patient_role = 'Teaching Staff'
elif 'staff' in purpose.lower() or 'employee' in purpose.lower():
    patient_role = 'Non-Teaching Staff'
elif 'president' in purpose.lower() or 'dean' in purpose.lower():
    patient_role = 'Administrator'
else:
    patient_role = 'Visitor'
```

## Files Modified
- `c:\xampp\htdocs\iClini V.2\app.py` - Lines 8983-9103

## Testing
To verify the fix:
1. Add a medical record for a Student → Should show with blue "Student" badge
2. Add a medical record for a Visitor (President/Dean/Staff) → Should show with orange "Visitor" badge
3. Both should appear in the consultations table
4. Refresh the consultations page to see all patient types

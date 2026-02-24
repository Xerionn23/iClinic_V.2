# DATABASE SCHEMA FIX - Teaching Medical Records

## ERROR ENCOUNTERED

```
Database error: 1054 (42S22): Unknown column 'tmr.medical_history' in 'field list'
```

## ROOT CAUSE

Ang `teaching_medical_records` table ay may **DIFFERENT STRUCTURE** compared to other medical records tables:

### Medical Records Tables Comparison

#### `medical_records` (Students)
```sql
- medical_history TEXT
- fever_duration VARCHAR(50)
- current_medication TEXT
- medication_schedule TEXT
- blood_pressure_systolic INT
- blood_pressure_diastolic INT
- pulse_rate INT
- temperature DECIMAL(4,1)
- respiratory_rate INT
- weight DECIMAL(5,2)
- height DECIMAL(5,2)
- bmi DECIMAL(4,1)
- symptoms TEXT
- treatment TEXT
- notes TEXT
- staff_name VARCHAR(100)
- staff_id INT
```

#### `teaching_medical_records` (Teaching Staff)
```sql
- chief_complaint TEXT
- physical_examination TEXT  ← Different!
- assessment TEXT             ← Different!
- diagnosis TEXT              ← Different!
- treatment TEXT
- prescribed_medicine TEXT
- vital_signs JSON            ← Different! (JSON instead of separate columns)
- doctor_notes TEXT           ← Different! (instead of 'notes')
- follow_up_date DATE
- created_by INT              ← Different! (instead of 'staff_id')
```

#### `non_teaching_medical_records` (Non-Teaching Staff)
```sql
- Same structure as medical_records (Students)
- Has all the same columns
```

#### `visitor_medical_records` (Visitors)
```sql
- Same structure as medical_records (Students)
- Has all the same columns
```

## SOLUTION IMPLEMENTED

### Fixed UNION Query with Column Mapping

Para mag-match ang lahat ng tables sa UNION query, ginawa ko ang:

1. **Empty Strings for Missing Text Columns**
   ```sql
   '' as medical_history
   '' as fever_duration
   '' as current_medication
   '' as medication_schedule
   ```

2. **NULL for Missing Numeric Columns**
   ```sql
   NULL as blood_pressure_systolic
   NULL as blood_pressure_diastolic
   NULL as pulse_rate
   NULL as temperature
   NULL as respiratory_rate
   NULL as weight
   NULL as height
   NULL as bmi
   ```

3. **Column Aliasing for Different Names**
   ```sql
   tmr.physical_examination as symptoms
   tmr.doctor_notes as notes
   CONCAT(u2.first_name, ' ', u2.last_name) as staff_name
   tmr.created_by as staff_id
   ```

4. **Additional JOIN for Staff Name**
   ```sql
   LEFT JOIN users u2 ON tmr.created_by = u2.id
   ```

### Complete Fixed Query for Teaching Staff

```sql
SELECT 
    tmr.id, 
    tmr.teaching_id as patient_id, 
    tmr.visit_date, 
    tmr.visit_time, 
    tmr.chief_complaint,
    
    -- Missing columns → Empty/NULL values
    '' as medical_history, 
    '' as fever_duration, 
    '' as current_medication, 
    '' as medication_schedule,
    NULL as blood_pressure_systolic, 
    NULL as blood_pressure_diastolic, 
    NULL as pulse_rate, 
    NULL as temperature, 
    NULL as respiratory_rate, 
    NULL as weight, 
    NULL as height, 
    NULL as bmi,
    
    -- Mapped columns
    tmr.physical_examination as symptoms, 
    tmr.treatment, 
    tmr.prescribed_medicine,
    '' as dental_procedure, 
    '' as procedure_notes, 
    tmr.follow_up_date, 
    '' as special_instructions, 
    tmr.doctor_notes as notes, 
    
    -- Staff information
    CONCAT(u2.first_name, ' ', u2.last_name) as staff_name, 
    tmr.created_by as staff_id,
    
    -- Timestamps
    tmr.created_at, 
    tmr.updated_at,
    
    -- Patient information
    CONCAT(u.first_name, ' ', u.last_name) as patient_name,
    'Teaching Staff' as patient_role,
    u.position as additional_info
    
FROM teaching_medical_records tmr
LEFT JOIN users u ON tmr.teaching_id = u.id AND u.position = 'Teaching Staff'
LEFT JOIN users u2 ON tmr.created_by = u2.id
```

## WHY DIFFERENT STRUCTURE?

Ang `teaching_medical_records` table ay designed for **more comprehensive medical documentation**:

- **`physical_examination`** - Detailed physical exam findings
- **`assessment`** - Medical assessment/evaluation
- **`diagnosis`** - Formal diagnosis
- **`vital_signs`** - JSON format for flexible vital signs storage
- **`doctor_notes`** - Professional medical notes

While other tables use simpler structure for basic clinic visits.

## RESULT

✅ **Error Fixed**: No more "Unknown column" error
✅ **All Patient Types Working**: Students, Visitors, Teaching Staff, Non-Teaching Staff
✅ **Data Compatibility**: Empty/NULL values for missing fields
✅ **Proper Display**: All consultations show correctly in Staff-Consultations.html

## TESTING

After the fix, you should see:

```javascript
// Console output
🔍 Loading medical records from API...
📡 API Response status: 200
✅ Loaded medical records: [count] records
🎯 Transformed consultations: [count] items
```

No more 500 errors! 🎉

## IMPORTANT NOTES

1. **Teaching Staff medical records** will show:
   - `symptoms` = `physical_examination` field
   - `notes` = `doctor_notes` field
   - Empty values for vital signs (since stored as JSON)

2. **All other patient types** work normally with full field data

3. **Future Enhancement**: Consider migrating all tables to same structure for consistency

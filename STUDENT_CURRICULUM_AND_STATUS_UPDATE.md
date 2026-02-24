# Student Database Update - Curriculum & Active Status

## Overview
Successfully updated the student database to support 7-year curriculum ranges and active/inactive student status tracking.

## Changes Implemented

### 1. Database Schema Updates

#### Added Columns:
- **`curriculum`** (VARCHAR 100): Stores curriculum year range (e.g., "2020-2027")
- **`is_active`** (BOOLEAN): Tracks whether student is currently enrolled
  - `TRUE` = Active/Enrolled student
  - `FALSE` = Inactive/Not enrolled student

### 2. Curriculum Format

**Old Format:** Single year (e.g., "2020")  
**New Format:** 7-year range (e.g., "2020-2027")

The curriculum range is automatically calculated from the student number:
- Student Number: `2020-0186`
- Curriculum: `2020-2027` (2020 + 7 years)

### 3. Active/Inactive Status

**Current Distribution:**
- ✅ **Active Students:** 62
- ❌ **Inactive Students:** 10
- 📊 **Total Students:** 72

**Inactive Students:**
1. 2018-0039
2. 2020-0041
3. 2017-0043
4. 2021-0037
5. 2025-0016
6. 2019-0042
7. 2022-0072
8. 2021-0052
9. 2016-0024
10. 2021-0030

## Sample Updated Records

| Student Number | Curriculum | Status |
|---------------|------------|---------|
| 2015-0014 | 2015-2022 | ✅ ACTIVE |
| 2015-0023 | 2015-2022 | ✅ ACTIVE |
| 2016-0024 | 2016-2023 | ❌ INACTIVE |
| 2017-0043 | 2017-2024 | ❌ INACTIVE |
| 2018-0039 | 2018-2025 | ❌ INACTIVE |
| 2019-0042 | 2019-2026 | ❌ INACTIVE |
| 2020-0041 | 2020-2027 | ❌ INACTIVE |

## Technical Details

### Migration Script
- **File:** `update_student_curriculum_and_status.py`
- **Execution:** Run once to update existing database
- **Safety:** Includes error handling and rollback capabilities

### Database Updates in app.py
- Updated `init_db()` function to include `is_active` column for new installations
- Automatic column addition for existing installations
- Default value: `TRUE` (active) for all new students

## Usage

### Filtering Active Students
```sql
-- Get only active students
SELECT * FROM students WHERE is_active = TRUE;

-- Get only inactive students
SELECT * FROM students WHERE is_active = FALSE;
```

### Curriculum Queries
```sql
-- Get students by curriculum year
SELECT * FROM students WHERE curriculum LIKE '2020%';

-- Get students graduating in specific year
SELECT * FROM students WHERE curriculum LIKE '%-2027';
```

## Benefits

1. **Better Student Tracking:** Easy to identify currently enrolled vs. graduated/transferred students
2. **Accurate Curriculum Management:** 7-year curriculum ranges match NC's actual program duration
3. **Improved Reporting:** Can generate reports for active students only
4. **Data Integrity:** Clear separation between current and former students
5. **Flexible Filtering:** Staff can filter patient lists by enrollment status

## Future Enhancements

Potential additions:
- Add enrollment date tracking
- Add graduation date for inactive students
- Add reason for inactive status (graduated, transferred, dropped out)
- Automated status updates based on curriculum end date

## Migration Summary

✅ **Successfully Completed:**
- Added `is_active` column to students table
- Added `curriculum` column to students table
- Updated all 72 student records with curriculum ranges (YYYY-YYYY format)
- Set 10 students as INACTIVE, 62 as ACTIVE
- Updated `app.py` init_db() function for future installations

**No data loss occurred during migration.**

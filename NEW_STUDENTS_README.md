# New Students Data - SQL Insert Guide

## 📋 Student Information Summary

### Student 1: Mary Joyce Pineda
- **Student Number**: 2022-0201
- **Full Name**: Mary Joyce Catahan Pineda
- **Gender**: Female
- **Birthdate**: March 12, 2002
- **Age**: 19
- **Email**: maryjoycepineda7@gmail.com
- **Course**: Bachelor of Science in Computer Science
- **Year Level**: 3rd Year
- **Curriculum**: 2022

### Student 2: Nizaniel Kate Lamadora
- **Student Number**: 2022-0220
- **Full Name**: Nizaniel Kate Ariaso Lamadora
- **Gender**: Female
- **Birthdate**: October 1, 2003
- **Age**: 18
- **Email**: nizanielkatelamadora@gmail.com
- **Course**: Bachelor of Science in Computer Science
- **Year Level**: 3rd Year
- **Curriculum**: 2022

### Student 3: Jeniebeth Sopeña
- **Student Number**: 2022-0516
- **Full Name**: Jeniebeth Solano Sopeña
- **Gender**: Female
- **Birthdate**: March 28, 2002
- **Age**: 16
- **Email**: jenibethsolano84@gmail.com
- **Course**: Bachelor of Science in Computer Science
- **Year Level**: 3rd Year
- **Curriculum**: 2022

## 🗂️ Database Table Structure

**Table Name**: `students`

**Key Columns Used**:
- `student_number` - Unique identifier (e.g., 2022-0201)
- `first_name` - Student's first name
- `last_name` - Student's surname
- `middle_name` - Student's middle name
- `gender` - Male/Female
- `date_of_birth` - Format: YYYY-MM-DD
- `age` - Integer
- `email` - Gmail address
- `course` - Degree program
- `curriculum` - Year of curriculum
- `level` - Year level (1st Year, 2nd Year, etc.)
- `student_status` - Active/Inactive
- `is_active` - Boolean (TRUE/FALSE)

**Columns Set to Default/NULL** (not provided in data):
- `picture` - NULL (no photo provided)
- `lrn` - NULL (Learner Reference Number)
- `suffix` - NULL (Jr., Sr., etc.)
- `place_of_birth` - Set to "Norzagaray, Bulacan"
- `nationality` - Set to "Filipino"
- `religion` - Set to "Roman Catholic"
- `province` - Set to "Bulacan"
- `city_municipality` - Set to "Norzagaray"
- `barangay` - Set to "Poblacion"
- `house_street` - NULL
- `mobile_no` - NULL
- `father_*` fields - NULL (no parent info provided)
- `mother_*` fields - NULL (no parent info provided)
- `department` - Set to "College of Computer Studies"
- `graduating` - Set to "No"

## 📝 How to Execute the SQL

### Method 1: Using phpMyAdmin
1. Open phpMyAdmin (http://localhost/phpmyadmin)
2. Select database `iclini_db`
3. Click on "SQL" tab
4. Copy and paste the contents from `INSERT_NEW_STUDENTS.sql`
5. Click "Go" to execute

### Method 2: Using MySQL Command Line
```bash
mysql -u root -p iclini_db < INSERT_NEW_STUDENTS.sql
```

### Method 3: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your database
3. Open `INSERT_NEW_STUDENTS.sql` file
4. Execute the script

## ✅ Verification

After inserting, run this query to verify:

```sql
SELECT 
    student_number,
    first_name,
    last_name,
    middle_name,
    gender,
    date_of_birth,
    age,
    email,
    course,
    level
FROM students 
WHERE student_number IN ('2022-0201', '2022-0220', '2022-0516')
ORDER BY student_number;
```

Expected result: 3 rows showing all three students.

## 🔐 Account Creation

After inserting students into database, they can create accounts:

1. Go to login page: http://127.0.0.1:5000/login
2. Click "Create Account"
3. Select role: **Student**
4. Enter their student number (e.g., 2022-0201)
5. System will send verification email to their Gmail
6. They click verification link and set their password
7. They can now login to iClinic system

## 📧 Gmail Addresses for Account Creation

The system will send verification emails to:
- maryjoycepineda7@gmail.com (Student 2022-0201)
- nizanielkatelamadora@gmail.com (Student 2022-0220)
- jenibethsolano84@gmail.com (Student 2022-0516)

## 🎯 Important Notes

1. **Student Numbers are Unique**: Cannot insert duplicate student numbers
2. **Email Format**: Must be valid Gmail addresses for verification
3. **Date Format**: Birthdates stored as YYYY-MM-DD in database
4. **Active Status**: All students set to Active by default
5. **Course Assignment**: All assigned to Computer Science (can be changed if needed)
6. **Year Level**: All set to 3rd Year based on 2022 curriculum

## 🔧 Troubleshooting

**If insert fails with "Duplicate entry" error:**
- Check if student number already exists
- Use this query to check:
```sql
SELECT * FROM students WHERE student_number IN ('2022-0201', '2022-0220', '2022-0516');
```

**If you need to update existing records instead:**
```sql
UPDATE students 
SET 
    first_name = 'Mary Joyce',
    last_name = 'Pineda',
    middle_name = 'Catahan',
    email = 'maryjoycepineda7@gmail.com'
WHERE student_number = '2022-0201';
```

## 📁 Files Created

1. `INSERT_NEW_STUDENTS.sql` - SQL insert statements
2. `NEW_STUDENTS_README.md` - This documentation file

---
**Created**: October 25, 2025
**Database**: iclini_db
**Table**: students
**Records**: 3 new students

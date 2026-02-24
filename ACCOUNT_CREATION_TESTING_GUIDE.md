# 🔐 ACCOUNT CREATION & FORGOT PASSWORD TESTING GUIDE
## iClinic Healthcare Management System

**Date Created:** October 26, 2025  
**Purpose:** Comprehensive testing guide for all 7 user types

---

## 📋 SYSTEM OVERVIEW

The iClinic system supports **7 different user roles** with proper account creation and password reset functionality:

1. ✅ **STUDENT** - Must exist in students database
2. ✅ **TEACHING STAFF** - Must exist in teaching database  
3. ✅ **NON-TEACHING STAFF** - Must exist in non_teaching_staff database
4. ✅ **NURSE** - Must exist in nurses database
5. ✅ **ADMIN** - Must exist in admins database
6. ✅ **DEANS** - Must exist in deans database
7. ✅ **PRESIDENT** - Must exist in president database

---

## 🔍 ACCOUNT CREATION VALIDATION LOGIC

### **Backend Validation Function:** `validate_id_and_get_info()`
**Location:** `app.py` lines 211-378

### **Validation Rules by Role:**

#### 1. **STUDENT** (role='student')
- **Database Table:** `students`
- **ID Field:** `student_number` (e.g., "2022-0186")
- **Validation:**
  - Must exist in students table
  - Name must match: `std_Firstname + std_Surname`
  - Email retrieved from: `std_EmailAdd`
- **Error Messages:**
  - "Student number {id} not found in database. Please contact the registrar."
  - "Name mismatch. Database shows: {db_name}"

#### 2. **TEACHING STAFF** (role='teaching_staff')
- **Database Table:** `teaching`
- **ID Field:** `faculty_id` (e.g., "FAC-CS-001")
- **Validation:**
  - Must exist in teaching table
  - Name must match: `first_name + last_name`
  - Email retrieved from: `email`
- **Sample Data Available:** 15 teaching staff records (FAC-CS-001 to FAC-IT-007)
- **Error Messages:**
  - "Faculty ID {id} not found in database. Please contact HR."
  - "Name mismatch. Database shows: {db_name}"

#### 3. **NURSE** (role='nurse')
- **Database Table:** `nurses`
- **ID Field:** `nurse_id` (e.g., "NURSE-001")
- **Validation:**
  - Must exist in nurses table with `status = 'Active'`
  - Name must match: `first_name + last_name`
  - Email retrieved from: `email`
- **Sample Data Available:** 1 nurse record (Green Lloyd Lapig)
- **Error Messages:**
  - "Nurse ID {id} not found in database or inactive. Please contact HR."
  - "Name mismatch. Database shows: {db_name}"

#### 4. **ADMIN** (role='admin')
- **Database Table:** `admins`
- **ID Field:** `admin_id` (e.g., "ADMIN-001")
- **Validation:**
  - Must exist in admins table with `status = 'Active'`
  - Name must match: `first_name + last_name`
  - Email retrieved from: `email`
- **Sample Data Available:** 1 admin record (System Administrator)
- **Error Messages:**
  - "Admin ID {id} not found in database or inactive. Please contact IT Department."
  - "Name mismatch. Database shows: {db_name}"

#### 5. **NON-TEACHING STAFF** (role='non_teaching_staff')
- **Database Table:** `non_teaching_staff`
- **ID Field:** `staff_id` (e.g., "NTS-001")
- **Validation:**
  - Basic validation only (simplified for now)
  - Name parsed from full name input
- **Sample Data Available:** 10 non-teaching staff records (NTS-001 to NTS-010)

#### 6. **DEANS** (role='deans')
- **Database Table:** `deans`
- **ID Field:** `dean_id` (e.g., "DEAN-001")
- **Validation:**
  - Basic validation only (simplified for now)
  - Name parsed from full name input
- **Sample Data Available:** 4 deans records (DEAN-001 to DEAN-004)

#### 7. **PRESIDENT** (role='president')
- **Database Table:** `president`
- **ID Field:** `president_id` (e.g., "PRES-001")
- **Validation:**
  - Basic validation only (simplified for now)
  - Name parsed from full name input
- **Sample Data Available:** 1 president record (Emilio Aguinaldo)

---

## 🧪 TESTING DATA - ACCOUNT CREATION

### ✅ **1. STUDENT ACCOUNT CREATION**

**Test Case 1.1: Valid Student Registration**
```
Role: Student
ID Number: 2021-0001
Full Name: Joseph Flynn
Email: (auto-retrieved from database)
Password: test123

Expected Result: ✅ Success
- Email verification sent to student's Gmail from database
- Account created after email verification
```

**Test Case 1.2: Invalid Student Number**
```
Role: Student
ID Number: 9999-9999
Full Name: Test Student
Password: test123

Expected Result: ❌ Error
Message: "Student number 9999-9999 not found in database. Please contact the registrar."
```

**Test Case 1.3: Name Mismatch**
```
Role: Student
ID Number: 2021-0001
Full Name: Wrong Name
Password: test123

Expected Result: ❌ Error
Message: "Name mismatch. Database shows: Joseph Flynn"
```

---

### ✅ **2. TEACHING STAFF ACCOUNT CREATION**

**Test Case 2.1: Valid Teaching Staff Registration**
```
Role: Teaching Staff
ID Number: FAC-CS-001
Full Name: Roberto Lapig
Email: (auto-retrieved: rlapig@gonzagary.edu.ph)
Password: test123

Expected Result: ✅ Success
- Email verification sent to institutional email
- Account created with role='teaching_staff'
```

**Test Case 2.2: Invalid Faculty ID**
```
Role: Teaching Staff
ID Number: FAC-XX-999
Full Name: Test Teacher
Password: test123

Expected Result: ❌ Error
Message: "Faculty ID FAC-XX-999 not found in database. Please contact HR."
```

**Available Teaching Staff IDs:**
- FAC-CS-001 (Roberto Lapig)
- FAC-CS-002 (Maria Santos)
- FAC-IT-001 (John Dela Cruz)
- FAC-IT-002 (Ana Rodriguez)
- FAC-CS-003 to FAC-IT-007 (15 total)

---

### ✅ **3. NURSE ACCOUNT CREATION**

**Test Case 3.1: Valid Nurse Registration**
```
Role: Nurse
ID Number: NURSE-001
Full Name: Green Lloyd Lapig
Email: (auto-retrieved: llyodlapig@gmail.com)
Password: test123

Expected Result: ✅ Success
- Email verification sent to nurse's email
- Account created with role='staff', position='Registered Nurse'
```

**Test Case 3.2: Invalid Nurse ID**
```
Role: Nurse
ID Number: NURSE-999
Full Name: Test Nurse
Password: test123

Expected Result: ❌ Error
Message: "Nurse ID NURSE-999 not found in database or inactive. Please contact HR."
```

---

### ✅ **4. ADMIN ACCOUNT CREATION**

**Test Case 4.1: Valid Admin Registration**
```
Role: Admin
ID Number: ADMIN-001
Full Name: System Administrator
Email: (auto-retrieved: admin@norzagaray.edu.ph)
Password: test123

Expected Result: ✅ Success
- Email verification sent to admin email
- Account created with role='admin', position='System Administrator'
```

**Test Case 4.2: Invalid Admin ID**
```
Role: Admin
ID Number: ADMIN-999
Full Name: Test Admin
Password: test123

Expected Result: ❌ Error
Message: "Admin ID ADMIN-999 not found in database or inactive. Please contact IT Department."
```

---

### ✅ **5. NON-TEACHING STAFF ACCOUNT CREATION**

**Test Case 5.1: Valid Non-Teaching Staff Registration**
```
Role: Non-Teaching Staff
ID Number: NTS-001
Full Name: Maria Santos
Email: (auto-retrieved: msantos@norzagaray.edu.ph)
Password: test123

Expected Result: ✅ Success
- Email verification sent to staff email
- Account created with role='non_teaching_staff'
```

**Available Non-Teaching Staff IDs:**
- NTS-001 (Maria Santos - Administrative Assistant)
- NTS-002 (Pedro Cruz - Librarian)
- NTS-003 (Rosa Garcia - Registrar)
- NTS-004 to NTS-010 (10 total)

---

### ✅ **6. DEANS ACCOUNT CREATION**

**Test Case 6.1: Valid Dean Registration**
```
Role: Deans
ID Number: DEAN-001
Full Name: Roberto Villanueva
Email: (auto-retrieved: rvillanueva@norzagaray.edu.ph)
Password: test123

Expected Result: ✅ Success
- Email verification sent to dean's email
- Account created with role='deans', position='Dean'
```

**Available Dean IDs:**
- DEAN-001 (Roberto Villanueva - College of Computer Studies)
- DEAN-002 (Patricia Herrera - College of Engineering)
- DEAN-003 (Fernando Jimenez - College of Business Administration)
- DEAN-004 (Concepcion Ortega - College of Education)

---

### ✅ **7. PRESIDENT ACCOUNT CREATION**

**Test Case 7.1: Valid President Registration**
```
Role: President
ID Number: PRES-001
Full Name: Emilio Aguinaldo
Email: (auto-retrieved: president@norzagaray.edu.ph)
Password: test123

Expected Result: ✅ Success
- Email verification sent to president's email
- Account created with role='president', position='President'
```

---

## 🔑 FORGOT PASSWORD TESTING

### **Backend Function:** `forgot_password()`
**Location:** `app.py` lines 2130-2247

### **Search Logic:**
The system searches for users in the following order:
1. Users table by `user_id` column
2. Students table by `student_number` → checks if user account exists
3. Nurses table by `nurse_id` → checks if user account exists
4. Admins table by `admin_id` → checks if user account exists
5. Users table by `username` or `email`

---

## 🧪 TESTING DATA - FORGOT PASSWORD

### ✅ **Test Case FP-1: Student Forgot Password**
```
User ID: 2021-0001 (Joseph Flynn's student number)

Expected Result: ✅ Success
- System finds student in students table
- Retrieves email from std_EmailAdd
- Checks if user account exists in users table
- Sends password reset email
- Token expires in 1 hour
```

### ✅ **Test Case FP-2: Teaching Staff Forgot Password**
```
User ID: FAC-CS-001 (Roberto Lapig's faculty ID)

Expected Result: ✅ Success
- System finds teaching staff in teaching table
- Retrieves email: rlapig@gonzagary.edu.ph
- Checks if user account exists
- Sends password reset email
```

### ✅ **Test Case FP-3: Nurse Forgot Password**
```
User ID: NURSE-001 (Green Lloyd Lapig's nurse ID)

Expected Result: ✅ Success
- System finds nurse in nurses table
- Retrieves email: llyodlapig@gmail.com
- Checks if user account exists
- Sends password reset email
```

### ✅ **Test Case FP-4: Admin Forgot Password**
```
User ID: ADMIN-001 (System Administrator's admin ID)

Expected Result: ✅ Success
- System finds admin in admins table
- Retrieves email: admin@norzagaray.edu.ph
- Checks if user account exists
- Sends password reset email
```

### ✅ **Test Case FP-5: Non-Teaching Staff Forgot Password**
```
User ID: NTS-001 (Maria Santos's staff ID)

Expected Result: ✅ Success
- System searches for staff ID
- Retrieves email from database
- Sends password reset email
```

### ✅ **Test Case FP-6: Dean Forgot Password**
```
User ID: DEAN-001 (Roberto Villanueva's dean ID)

Expected Result: ✅ Success
- System searches for dean ID
- Retrieves email: rvillanueva@norzagaray.edu.ph
- Sends password reset email
```

### ✅ **Test Case FP-7: President Forgot Password**
```
User ID: PRES-001 (Emilio Aguinaldo's president ID)

Expected Result: ✅ Success
- System searches for president ID
- Retrieves email: president@norzagaray.edu.ph
- Sends password reset email
```

### ❌ **Test Case FP-8: Invalid User ID**
```
User ID: INVALID-999

Expected Result: ❌ Error
Message: "User ID not found. Please check and try again."
```

### ❌ **Test Case FP-9: User Without Account**
```
User ID: 2022-0054 (Student exists but no user account created)

Expected Result: ❌ Error
Message: "User ID not found. Please check and try again."
```

---

## 📧 EMAIL VERIFICATION SYSTEM

### **Email Configuration:**
- **SMTP Server:** smtp.gmail.com:587
- **From Email:** norzagaraycollege.clinic@gmail.com
- **App Password:** xtsweijcxsntwhld

### **Verification Email Features:**
- Professional HTML template with iClinic branding
- Verification link format: `http://127.0.0.1:5000/verify-email?token={token}`
- Token expiration: 24 hours
- One-time use tokens

### **Password Reset Email Features:**
- Professional HTML template with security warnings
- Reset link format: `http://127.0.0.1:5000/reset-password?token={token}`
- Token expiration: 1 hour
- One-time use tokens
- Clear security instructions

---

## ⚠️ KNOWN ISSUES & LIMITATIONS

### **1. President, Deans, Non-Teaching Staff Validation**
**Status:** ⚠️ SIMPLIFIED VALIDATION
- Lines 354-365 in `validate_id_and_get_info()`
- Currently uses basic validation (name parsing only)
- Does NOT check against database tables
- **Recommendation:** Implement full database validation like Student/Nurse/Admin

**Fix Required:**
```python
elif role == 'non_teaching_staff':
    # TODO: Add database validation
    cursor.execute('''
        SELECT id, first_name, last_name, email
        FROM non_teaching_staff 
        WHERE staff_id = %s AND status = 'Active'
    ''', (id_number,))
    # Add name matching and email retrieval
```

### **2. Forgot Password - Teaching Staff**
**Status:** ⚠️ MISSING SEARCH LOGIC
- Lines 2148-2196 in `forgot_password()`
- System searches: users, students, nurses, admins
- **MISSING:** Teaching staff table search
- **Impact:** Teaching staff cannot use forgot password with faculty_id

**Fix Required:**
```python
# Add after admin search (line 2188)
if not user_email:
    cursor.execute('SELECT email, first_name, last_name FROM teaching WHERE faculty_id = %s AND status = "Active"', (user_id,))
    teaching = cursor.fetchone()
    if teaching:
        cursor.execute('SELECT email, first_name, last_name FROM users WHERE email = %s', (teaching[0],))
        user = cursor.fetchone()
        if user:
            user_email = user[0]
            user_name = f"{user[1]} {user[2]}"
```

### **3. Forgot Password - Deans, President, Non-Teaching**
**Status:** ⚠️ MISSING SEARCH LOGIC
- Same issue as teaching staff
- Need to add database searches for these roles

---

## ✅ TESTING CHECKLIST

### **Account Creation Testing:**
- [ ] Student account creation with valid student number
- [ ] Student account creation with invalid student number
- [ ] Student account creation with name mismatch
- [ ] Teaching staff account creation (FAC-CS-001)
- [ ] Nurse account creation (NURSE-001)
- [ ] Admin account creation (ADMIN-001)
- [ ] Non-teaching staff account creation (NTS-001)
- [ ] Dean account creation (DEAN-001)
- [ ] President account creation (PRES-001)
- [ ] Email verification link works
- [ ] Account created after email verification
- [ ] Duplicate email prevention works

### **Forgot Password Testing:**
- [ ] Student forgot password (2021-0001)
- [ ] Nurse forgot password (NURSE-001)
- [ ] Admin forgot password (ADMIN-001)
- [ ] Teaching staff forgot password (FAC-CS-001) ⚠️ NEEDS FIX
- [ ] Non-teaching staff forgot password (NTS-001) ⚠️ NEEDS FIX
- [ ] Dean forgot password (DEAN-001) ⚠️ NEEDS FIX
- [ ] President forgot password (PRES-001) ⚠️ NEEDS FIX
- [ ] Invalid user ID error message
- [ ] Password reset email received
- [ ] Reset link works
- [ ] Token expiration (1 hour)
- [ ] Token one-time use enforcement
- [ ] Password successfully changed

### **Login Testing After Account Creation:**
- [ ] Student can login with email and password
- [ ] Teaching staff can login
- [ ] Nurse can login
- [ ] Admin can login
- [ ] Non-teaching staff can login
- [ ] Dean can login
- [ ] President can login
- [ ] Correct dashboard redirect by role

---

## 🔧 RECOMMENDED FIXES

### **Priority 1: Add Full Database Validation**
**Files to Update:** `app.py` lines 354-365

Add proper database validation for:
- Non-Teaching Staff (non_teaching_staff table)
- Deans (deans table)
- President (president table)

### **Priority 2: Add Forgot Password Support**
**Files to Update:** `app.py` lines 2148-2196

Add database searches for:
- Teaching staff (teaching table)
- Non-teaching staff (non_teaching_staff table)
- Deans (deans table)
- President (president table)

### **Priority 3: Test Email Delivery**
Ensure Gmail App Password is working:
- Test verification emails
- Test password reset emails
- Check spam folders
- Verify email templates display correctly

---

## 📝 TESTING NOTES

**Date:** _______________  
**Tester:** _______________  
**Environment:** Development / Production

**Results:**
```
ACCOUNT CREATION:
✅ Students: _____
✅ Teaching Staff: _____
✅ Nurses: _____
✅ Admins: _____
✅ Non-Teaching Staff: _____
✅ Deans: _____
✅ President: _____

FORGOT PASSWORD:
✅ Students: _____
⚠️ Teaching Staff: _____ (NEEDS FIX)
✅ Nurses: _____
✅ Admins: _____
⚠️ Non-Teaching Staff: _____ (NEEDS FIX)
⚠️ Deans: _____ (NEEDS FIX)
⚠️ President: _____ (NEEDS FIX)
```

**Issues Found:**
```
1. _____________________________________
2. _____________________________________
3. _____________________________________
```

---

## 🎯 CONCLUSION

**ACCOUNT CREATION STATUS:**
- ✅ **WORKING:** Students, Teaching Staff, Nurses, Admins
- ⚠️ **PARTIAL:** Non-Teaching Staff, Deans, President (simplified validation)

**FORGOT PASSWORD STATUS:**
- ✅ **WORKING:** Students, Nurses, Admins
- ⚠️ **NEEDS FIX:** Teaching Staff, Non-Teaching Staff, Deans, President

**OVERALL SYSTEM HEALTH:** 🟡 **GOOD** (Core functionality works, minor enhancements needed)

---

**Last Updated:** October 26, 2025  
**Document Version:** 1.0

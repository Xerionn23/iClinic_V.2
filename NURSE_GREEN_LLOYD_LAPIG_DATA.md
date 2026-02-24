# Nurse Green Lloyd Lapig - Sample Data Created

## Overview
Successfully created sample data for **Nurse Green Lloyd Lapig** in the nurses table with complete profile information and user account.

## Nurse Profile Data

### Personal Information
- **Nurse ID**: `NURSE-001`
- **Employee Number**: `E3001`
- **Full Name**: Green Lloyd M. Lapig
  - First Name: `Green Lloyd`
  - Last Name: `Lapig`
  - Middle Name: `M.`
- **Email**: `llyodlapig@gmail.com`
- **Gender**: `Male`
- **Age**: `28`
- **Blood Type**: `O+`

### Professional Information
- **Position**: `Registered Nurse`
- **Department**: `Clinic`
- **Status**: `Active`
- **Hire Date**: `2020-06-15`
- **License Number**: `PRC-123456`
- **Specialization**: `General Nursing`

### Contact Information
- **Contact Number**: `09171234567`
- **Address**: `Norzagaray, Bulacan`

### Emergency Contact
- **Emergency Contact Name**: `Maria Lapig`
- **Relationship**: `Mother`
- **Emergency Contact Number**: `09181234568`

### Medical Information
- **Allergies**: `None`
- **Medical Conditions**: `None`

### System Information
- **Is Archived**: `FALSE` (Active in system)
- **Created At**: Auto-generated timestamp
- **Updated At**: Auto-generated timestamp

## User Account Information

### Login Credentials
- **Username**: `llyodlapig@gmail.com`
- **Email**: `llyodlapig@gmail.com`
- **Password**: `staff123`
- **Role**: `staff`
- **Position**: `Registered Nurse`

### How to Login
1. Go to login page
2. Enter User ID: `NURSE-001` or `llyodlapig@gmail.com`
3. Enter Password: `staff123`
4. Click Sign In
5. Will redirect to Staff Dashboard

## Login Options

### Option 1: Using Nurse ID
- **User ID**: `NURSE-001`
- **Password**: `staff123`

### Option 2: Using Email
- **User ID**: `llyodlapig@gmail.com`
- **Password**: `staff123`

### Option 3: Using Username
- **User ID**: `llyodlapig@gmail.com`
- **Password**: `staff123`

## Database Tables

### Nurses Table Entry
```sql
INSERT INTO nurses (
    nurse_id, employee_number, first_name, last_name, middle_name, 
    email, position, department, status, hire_date, age, gender, 
    contact_number, address, blood_type, emergency_contact_name, 
    emergency_contact_relationship, emergency_contact_number, 
    allergies, medical_conditions, license_number, specialization, is_archived
) VALUES (
    'NURSE-001', 'E3001', 'Green Lloyd', 'Lapig', 'M.',
    'llyodlapig@gmail.com', 'Registered Nurse', 'Clinic', 
    'Active', '2020-06-15', 28, 'Male', '09171234567',
    'Norzagaray, Bulacan', 'O+', 'Maria Lapig', 'Mother', 
    '09181234568', 'None', 'None', 'PRC-123456', 'General Nursing', FALSE
);
```

### Users Table Entry
```sql
INSERT INTO users (
    username, email, password_hash, role, first_name, last_name, position
) VALUES (
    'llyodlapig@gmail.com', 
    'llyodlapig@gmail.com', 
    'hashed_password_for_staff123', 
    'staff', 
    'Green Lloyd', 
    'Lapig', 
    'Registered Nurse'
);
```

## Features

### Professional Credentials
✅ **PRC License Number**: PRC-123456
✅ **Specialization**: General Nursing
✅ **Department**: Clinic
✅ **Position**: Registered Nurse

### System Access
✅ Can login using Nurse ID (NURSE-001)
✅ Can login using email (llyodlapig@gmail.com)
✅ Has staff role with appropriate permissions
✅ Access to Staff Dashboard

### Medical Records
✅ Can have own medical records in `nurse_medical_records` table
✅ Complete vital signs tracking
✅ Clinic stay management
✅ Admission/discharge time tracking

## Automatic Creation

This data is automatically created when:
1. The application starts for the first time
2. The `init_db()` function runs
3. The nurses table is empty

The system will:
- Check if nurses table is empty
- Insert Green Lloyd Lapig's data
- Create corresponding user account
- Print confirmation: "✅ Added nurse: Green Lloyd Lapig (NURSE-001)"

## Testing

### Test Login with Nurse ID
```
1. Open login page
2. User ID: NURSE-001
3. Password: staff123
4. Expected: Login successful, redirect to Staff Dashboard
```

### Test Login with Email
```
1. Open login page
2. User ID: llyodlapig@gmail.com
3. Password: staff123
4. Expected: Login successful, redirect to Staff Dashboard
```

### Verify Nurse Profile
```sql
SELECT * FROM nurses WHERE nurse_id = 'NURSE-001';
```

### Verify User Account
```sql
SELECT * FROM users WHERE email = 'llyodlapig@gmail.com';
```

## Additional Notes

### Password Security
- Password is hashed using `generate_password_hash('staff123')`
- Secure bcrypt hashing algorithm
- Password never stored in plain text

### Email Correction
- Previous email typo: `llyodlapit@gmail.com` (wrong)
- Corrected email: `llyodlapig@gmail.com` (correct)
- Now matches the nurse's actual email

### Professional License
- PRC License: PRC-123456
- Valid for Registered Nurse
- Can be updated as needed

### Emergency Contact
- Mother: Maria Lapig
- Contact: 09181234568
- Relationship documented for emergencies

## Summary

✅ **Nurse Profile Created**: Green Lloyd M. Lapig
✅ **Nurse ID**: NURSE-001
✅ **User Account**: llyodlapig@gmail.com
✅ **Password**: staff123
✅ **Login Methods**: Nurse ID, Email, Username
✅ **Professional License**: PRC-123456
✅ **Department**: Clinic
✅ **Status**: Active
✅ **Complete Profile**: All fields populated with realistic data

The nurse can now login to the system and access all staff features! 🏥👨‍⚕️

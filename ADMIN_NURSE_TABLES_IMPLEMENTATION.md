# Admin and Nurse Tables Implementation

## Overview
Successfully created separate database tables for **Admins** and **Nurses** with their own unique ID numbers (Admin ID and Nurse ID), following the same structure as Teaching Staff and Non-Teaching Staff tables.

## Database Tables Created

### 1. Nurses Table
**Table Name**: `nurses`

**Columns**:
- `id` - INT AUTO_INCREMENT PRIMARY KEY
- `nurse_id` - VARCHAR(20) UNIQUE NOT NULL (e.g., NURSE-001, NURSE-002)
- `employee_number` - VARCHAR(20)
- `first_name` - VARCHAR(50) NOT NULL
- `last_name` - VARCHAR(50) NOT NULL
- `middle_name` - VARCHAR(50)
- `email` - VARCHAR(100) UNIQUE NOT NULL
- `position` - VARCHAR(100) DEFAULT 'Nurse'
- `department` - VARCHAR(100) DEFAULT 'Clinic'
- `status` - ENUM('Active', 'Inactive', 'On Leave') DEFAULT 'Active'
- `hire_date` - DATE
- `age` - INT
- `gender` - ENUM('Male', 'Female', 'Other') DEFAULT 'Female'
- `contact_number` - VARCHAR(20)
- `address` - TEXT
- `blood_type` - VARCHAR(10)
- `emergency_contact_name` - VARCHAR(100)
- `emergency_contact_relationship` - VARCHAR(50)
- `emergency_contact_number` - VARCHAR(20)
- `allergies` - TEXT
- `medical_conditions` - TEXT
- `license_number` - VARCHAR(50) - **Nurse-specific field**
- `specialization` - VARCHAR(100) - **Nurse-specific field**
- `is_archived` - BOOLEAN DEFAULT FALSE
- `created_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

**Special Features**:
- Includes `license_number` for professional nursing license
- Includes `specialization` for nursing specialization (e.g., Pediatric, Emergency, etc.)
- Default department is 'Clinic'

### 2. Nurse Medical Records Table
**Table Name**: `nurse_medical_records`

**Purpose**: Track medical records for nurses who visit the clinic as patients

**Columns**: Same structure as student/teaching/non-teaching medical records
- Complete vital signs tracking
- Clinic stay management
- Admission and discharge time tracking
- Foreign key relationship with `nurses` table

### 3. Admins Table
**Table Name**: `admins`

**Columns**:
- `id` - INT AUTO_INCREMENT PRIMARY KEY
- `admin_id` - VARCHAR(20) UNIQUE NOT NULL (e.g., ADMIN-001, ADMIN-002)
- `employee_number` - VARCHAR(20)
- `first_name` - VARCHAR(50) NOT NULL
- `last_name` - VARCHAR(50) NOT NULL
- `middle_name` - VARCHAR(50)
- `email` - VARCHAR(100) UNIQUE NOT NULL
- `position` - VARCHAR(100) DEFAULT 'System Administrator'
- `department` - VARCHAR(100) DEFAULT 'IT Department'
- `status` - ENUM('Active', 'Inactive', 'On Leave') DEFAULT 'Active'
- `hire_date` - DATE
- `age` - INT
- `gender` - ENUM('Male', 'Female', 'Other') DEFAULT 'Male'
- `contact_number` - VARCHAR(20)
- `address` - TEXT
- `blood_type` - VARCHAR(10)
- `emergency_contact_name` - VARCHAR(100)
- `emergency_contact_relationship` - VARCHAR(50)
- `emergency_contact_number` - VARCHAR(20)
- `allergies` - TEXT
- `medical_conditions` - TEXT
- `access_level` - VARCHAR(50) DEFAULT 'Full Access' - **Admin-specific field**
- `is_archived` - BOOLEAN DEFAULT FALSE
- `created_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

**Special Features**:
- Includes `access_level` for system access permissions
- Default position is 'System Administrator'
- Default department is 'IT Department'

### 4. Admin Medical Records Table
**Table Name**: `admin_medical_records`

**Purpose**: Track medical records for admins who visit the clinic as patients

**Columns**: Same structure as other medical records tables
- Complete vital signs tracking
- Clinic stay management
- Admission and discharge time tracking
- Foreign key relationship with `admins` table

## Login System Integration

### Enhanced Authentication Flow
The login system now supports **5 types of User IDs**:

1. **Student Number** (e.g., `2021-0001`, `2022-0186`)
   - Checks `students` table by `student_number`
   - Links to user account via email

2. **Nurse ID** (e.g., `NURSE-001`, `NURSE-002`)
   - Checks `nurses` table by `nurse_id`
   - Links to user account via email
   - Validates status is 'Active'

3. **Admin ID** (e.g., `ADMIN-001`, `ADMIN-002`)
   - Checks `admins` table by `admin_id`
   - Links to user account via email
   - Validates status is 'Active'

4. **Staff Username/Email**
   - Checks `users` table by username or email
   - For teaching staff, non-teaching staff, etc.

5. **Legacy Username**
   - Backward compatibility with existing accounts

### Authentication Priority Order
```
1. Check student_number in students table
   ↓ (if not found)
2. Check nurse_id in nurses table
   ↓ (if not found)
3. Check admin_id in admins table
   ↓ (if not found)
4. Check username/email in users table
   ↓
5. Verify password and create session
```

## ID Format Examples

### Nurse IDs
- `NURSE-001` - First nurse
- `NURSE-002` - Second nurse
- `NURSE-003` - Third nurse
- Format: `NURSE-XXX` (3-digit number)

### Admin IDs
- `ADMIN-001` - First admin
- `ADMIN-002` - Second admin
- `ADMIN-003` - Third admin
- Format: `ADMIN-XXX` (3-digit number)

### Comparison with Other IDs
- **Students**: `2022-0186` (Year-Number)
- **Teaching Staff**: `FAC-CS-001` (Faculty-Department-Number)
- **Non-Teaching Staff**: `NTS-001` (NonTeachingStaff-Number)
- **Deans**: `DEAN-001` (Dean-Number)
- **President**: `PRES-001` (President-Number)
- **Nurses**: `NURSE-001` (Nurse-Number)
- **Admins**: `ADMIN-001` (Admin-Number)

## Database Relationships

### Foreign Key Relationships
```
nurses table
  ↓ (id)
nurse_medical_records table (nurse_id)
  ↓ (staff_id)
users table

admins table
  ↓ (id)
admin_medical_records table (admin_id)
  ↓ (staff_id)
users table
```

### User Account Linking
All nurses and admins must have corresponding entries in the `users` table:
- Linked via `email` field
- Users table stores authentication credentials
- Nurses/Admins tables store detailed profile information

## How to Add Nurses and Admins

### Adding a Nurse
```sql
-- 1. Insert into nurses table
INSERT INTO nurses (
    nurse_id, employee_number, first_name, last_name, middle_name, 
    email, position, department, status, hire_date, age, gender, 
    contact_number, address, blood_type, license_number, specialization
) VALUES (
    'NURSE-001', 'E3001', 'Maria', 'Santos', 'L.',
    'msantos@norzagaray.edu.ph', 'Registered Nurse', 'Clinic', 
    'Active', '2020-01-15', 32, 'Female', '09171234567',
    'Norzagaray, Bulacan', 'O+', 'PRC-12345', 'General Nursing'
);

-- 2. Create user account (if not exists)
INSERT INTO users (
    username, email, password_hash, role, 
    first_name, last_name, position
) VALUES (
    'msantos', 'msantos@norzagaray.edu.ph', 
    'hashed_password_here', 'staff',
    'Maria', 'Santos', 'Registered Nurse'
);
```

### Adding an Admin
```sql
-- 1. Insert into admins table
INSERT INTO admins (
    admin_id, employee_number, first_name, last_name, middle_name,
    email, position, department, status, hire_date, age, gender,
    contact_number, address, blood_type, access_level
) VALUES (
    'ADMIN-001', 'E4001', 'John', 'Doe', 'A.',
    'jdoe@norzagaray.edu.ph', 'System Administrator', 'IT Department',
    'Active', '2019-01-10', 35, 'Male', '09181234567',
    'Norzagaray, Bulacan', 'A+', 'Full Access'
);

-- 2. Create user account (if not exists)
INSERT INTO users (
    username, email, password_hash, role,
    first_name, last_name, position
) VALUES (
    'jdoe', 'jdoe@norzagaray.edu.ph',
    'hashed_password_here', 'admin',
    'John', 'Doe', 'System Administrator'
);
```

## Login Examples

### Nurse Login
- **User ID**: `NURSE-001`
- **Password**: Nurse's password
- System checks nurses table → finds email → checks users table → authenticates

### Admin Login
- **User ID**: `ADMIN-001`
- **Password**: Admin's password
- System checks admins table → finds email → checks users table → authenticates

### Legacy Admin Login (Still Supported)
- **User ID**: `ADMIN` (username)
- **Password**: `ADMIN123`
- System checks users table directly → authenticates

## Benefits

1. **Consistent Structure**: Nurses and Admins now have the same detailed structure as other staff
2. **Unique Identification**: Each nurse and admin has a unique ID number
3. **Medical Records**: Can track medical records for nurses and admins as patients
4. **Professional Data**: Includes license numbers for nurses and access levels for admins
5. **Easy Management**: Separate tables make it easy to manage different staff types
6. **Login Flexibility**: Can login using Nurse ID, Admin ID, or email/username

## Frontend Updates

### Login Page
- Updated placeholder: "Student Number / Nurse ID / Admin ID / Staff Number"
- Updated helper text to include Nurse ID and Admin ID
- Credit card icon represents all types of ID cards

### Registration (Future Enhancement)
- Can add Nurse and Admin registration options
- Would follow same pattern as teaching/non-teaching staff registration

## Medical Records Integration

### When Nurses/Admins Visit Clinic
1. Staff can add medical records using nurse_medical_records or admin_medical_records tables
2. Same fields as student medical records (vital signs, diagnosis, treatment, etc.)
3. Supports clinic stay tracking with admission/discharge times
4. Complete medical history for all staff members

## Security Considerations

1. **Active Status Check**: Only active nurses and admins can login
2. **Email Verification**: Requires matching email in users table
3. **Password Hashing**: All passwords stored as secure hashes
4. **Role-Based Access**: Different roles have different dashboard access
5. **Audit Trail**: Created_at and updated_at timestamps for all records

## Testing

### Test Nurse Login
1. Add a nurse to nurses table with nurse_id = 'NURSE-001'
2. Create corresponding user account with same email
3. Login with User ID: `NURSE-001` and password
4. Should redirect to appropriate dashboard based on role

### Test Admin Login
1. Add an admin to admins table with admin_id = 'ADMIN-001'
2. Create corresponding user account with same email
3. Login with User ID: `ADMIN-001` and password
4. Should redirect to admin dashboard

## Future Enhancements

1. **Bulk Import**: Add CSV import for nurses and admins
2. **Profile Management**: Dedicated pages for managing nurse/admin profiles
3. **License Tracking**: Automatic alerts for license expiration
4. **Access Control**: Granular permissions based on access_level
5. **Shift Management**: Track nurse schedules and shifts
6. **Performance Metrics**: Track admin system activities

## Summary

✅ **Nurses Table**: Created with nurse_id and nurse-specific fields (license_number, specialization)
✅ **Nurse Medical Records**: Complete medical tracking for nurses as patients
✅ **Admins Table**: Created with admin_id and admin-specific fields (access_level)
✅ **Admin Medical Records**: Complete medical tracking for admins as patients
✅ **Login Integration**: Support for Nurse ID and Admin ID authentication
✅ **Consistent Structure**: Same columns as teaching/non-teaching staff tables
✅ **Professional Features**: License numbers, specializations, access levels included

The system now has complete support for Nurses and Admins with their own unique ID numbers, exactly as requested! 🏥👨‍⚕️👩‍⚕️

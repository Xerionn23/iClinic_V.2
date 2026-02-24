# Nurse and Admin Registration System

## Overview
Successfully added **Nurse** and **Admin** roles to the iClinic registration system. Both roles now have proper database validation and can create accounts through the registration form.

## Changes Made

### 1. Frontend Updates (login.html)

#### Added Nurse and Admin to Role Dropdown
- Nurse option added
- Admin option added

**Complete Role Options:**
1. Student
2. Nurse (NEW)
3. Admin (NEW)
4. President
5. Deans
6. Teaching Staff
7. Non-Teaching Staff

#### Dynamic ID Field Labels

**For Nurse:**
- Label: "Nurse ID"
- Placeholder: "Enter your nurse ID (e.g., NURSE-001)"
- Pattern: NURSE-[0-9]{3}
- Format: NURSE-NNN

**For Admin:**
- Label: "Admin ID"
- Placeholder: "Enter your admin ID (e.g., ADMIN-001)"
- Pattern: ADMIN-[0-9]{3}
- Format: ADMIN-NNN

### 2. Backend Updates (app.py)

#### Enhanced validate_id_and_get_info() Function

**Nurse Validation:**
- Checks nurses table for nurse_id
- Validates status is 'Active'
- Verifies name matches database
- Returns nurse info including email, position, license_number

**Admin Validation:**
- Checks admins table for admin_id
- Validates status is 'Active'
- Verifies name matches database
- Returns admin info including email, position, access_level

#### Updated Role and Position Mapping

**Role Map:**
- nurse: 'staff' (Nurses get staff role)
- admin: 'admin' (Admins get admin role)

**Position Map:**
- nurse: 'Registered Nurse'
- admin: 'System Administrator'

## Registration Flow

### For Nurses

1. Nurse profile must exist in nurses table
2. User selects "Nurse" role
3. Enters Nurse ID (e.g., NURSE-001)
4. Enters full name (must match database)
5. System validates against nurses table
6. Verification email sent to registered email
7. User clicks verification link
8. Account created with staff role

### For Admins

1. Admin profile must exist in admins table
2. User selects "Admin" role
3. Enters Admin ID (e.g., ADMIN-001)
4. Enters full name (must match database)
5. System validates against admins table
6. Verification email sent to registered email
7. User clicks verification link
8. Account created with admin role

## Example: Nurse Green Lloyd Lapig Registration

**Database Record:**
- nurse_id: NURSE-001
- first_name: Green Lloyd
- last_name: Lapig
- email: llyodlapig@gmail.com
- status: Active

**Registration Steps:**
1. Select Role: Nurse
2. Enter Nurse ID: NURSE-001
3. Enter Full Name: Green Lloyd Lapig
4. Enter Password
5. System validates and sends email to llyodlapig@gmail.com
6. Click verification link
7. Account created with staff role
8. Can login with NURSE-001 or email

## Validation Rules

### Nurse Registration
- Must have valid Nurse ID in database
- Status must be 'Active'
- Name must match database record
- Email from database is used

### Admin Registration
- Must have valid Admin ID in database
- Status must be 'Active'
- Name must match database record
- Email from database is used

## Security Features

- Database validation required
- Status check (only Active users)
- Name verification
- Email from database (not user input)
- Password hashing
- Duplicate email prevention

## Summary

Frontend: Added Nurse and Admin to registration form
Validation: Checks nurses/admins tables for valid IDs
Name Verification: Ensures name matches database
Email Security: Uses email from database
Role Mapping: Proper role assignment
Login Integration: Works with User ID login system

Nurses and Admins can now register accounts with full database validation!

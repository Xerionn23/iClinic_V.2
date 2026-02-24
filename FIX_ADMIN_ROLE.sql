-- ✅ FIX ADMIN ROLE - Run this in phpMyAdmin SQL tab

-- Step 1: Check current role
SELECT 
    id,
    user_id,
    email,
    role,
    position,
    CONCAT(first_name, ' ', last_name) as full_name,
    created_at
FROM users 
WHERE user_id = 'ADMIN-002';

-- Step 2: Update role from 'user' to 'admin' AND position to 'System Admin'
UPDATE users 
SET role = 'admin',
    position = 'System Admin'
WHERE user_id = 'ADMIN-002';

-- Step 3: Verify the fix
SELECT 
    id,
    user_id,
    email,
    role,
    position,
    CONCAT(first_name, ' ', last_name) as full_name,
    created_at
FROM users 
WHERE user_id = 'ADMIN-002';

-- Expected result after fix:
-- role should be: 'admin'
-- position should be: 'System Admin'

-- ============================================================================
-- POPULATE USER_ID FOR EXISTING USERS
-- Run this SQL script in phpMyAdmin to update all NULL user_id values
-- ============================================================================

-- 1. Update llyodlapig@gmail.com (Staff/Nurse)
-- Check if exists in nurses table first
UPDATE users u
LEFT JOIN nurses n ON u.email = n.email
SET u.user_id = n.nurse_id
WHERE u.email = 'llyodlapig@gmail.com' AND n.nurse_id IS NOT NULL;

-- If not in nurses table, set a default staff ID
UPDATE users
SET user_id = 'STAFF-001'
WHERE email = 'llyodlapig@gmail.com' AND user_id IS NULL;

-- 2. Update student accounts
-- Try to match by email
UPDATE users u
INNER JOIN students s ON u.email = s.std_EmailAdd
SET u.user_id = s.student_number
WHERE u.role = 'student' AND u.user_id IS NULL;

-- 3. If students still have NULL, assign temporary IDs
-- (You can update these manually later with correct student numbers)
UPDATE users
SET user_id = CONCAT('TEMP-STU-', id)
WHERE role = 'student' AND user_id IS NULL;

-- 4. Update teaching staff
UPDATE users u
INNER JOIN teaching t ON u.email = t.email
SET u.user_id = t.faculty_id
WHERE u.role = 'teaching_staff' AND u.user_id IS NULL;

-- If still NULL, assign temporary IDs
UPDATE users
SET user_id = CONCAT('FAC-', LPAD(id, 3, '0'))
WHERE role = 'teaching_staff' AND user_id IS NULL;

-- 5. Update president and deans
UPDATE users u
INNER JOIN president p ON u.email = p.email
SET u.user_id = p.president_id
WHERE u.role = 'president' AND u.user_id IS NULL;

UPDATE users u
INNER JOIN deans d ON u.email = d.email
SET u.user_id = d.dean_id
WHERE u.role = 'deans' AND u.user_id IS NULL;

-- ============================================================================
-- VERIFICATION QUERY - Run this to check results
-- ============================================================================
SELECT 
    id,
    user_id,
    username,
    email,
    role,
    CASE 
        WHEN user_id IS NULL THEN '❌ NULL'
        WHEN user_id LIKE 'TEMP-%' THEN '⚠️ TEMPORARY'
        ELSE '✅ OK'
    END as status
FROM users
ORDER BY id;

-- ============================================================================
-- Count users by status
-- ============================================================================
SELECT 
    CASE 
        WHEN user_id IS NULL THEN 'NULL'
        WHEN user_id LIKE 'TEMP-%' THEN 'TEMPORARY'
        ELSE 'OK'
    END as status,
    COUNT(*) as count
FROM users
GROUP BY status;

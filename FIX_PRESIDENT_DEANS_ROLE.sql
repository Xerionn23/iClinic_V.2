-- Fix existing President/Deans accounts that were created with wrong role
-- These accounts were saved as 'staff' instead of 'president' or 'deans'

-- Update President accounts (position = 'President' but role = 'staff')
UPDATE users 
SET role = 'president' 
WHERE position = 'President' AND role = 'staff';

-- Update Deans accounts (position = 'Dean' but role = 'staff')
UPDATE users 
SET role = 'deans' 
WHERE position = 'Dean' AND role = 'staff';

-- Verify the changes
SELECT id, username, email, role, position, first_name, last_name
FROM users 
WHERE role IN ('president', 'deans')
ORDER BY role, username;

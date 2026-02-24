-- Update announcement priorities from old values to new values
-- This script updates the priority ENUM values in the announcements table

-- First, modify the column to allow both old and new values temporarily
ALTER TABLE announcements 
MODIFY COLUMN priority ENUM('low', 'medium', 'high', 'standard', 'important', 'urgent') DEFAULT 'important';

-- Update the data: map old values to new values
UPDATE announcements SET priority = 'urgent' WHERE priority = 'high';
UPDATE announcements SET priority = 'important' WHERE priority = 'medium';
UPDATE announcements SET priority = 'standard' WHERE priority = 'low';

-- Finally, remove the old values from the ENUM
ALTER TABLE announcements 
MODIFY COLUMN priority ENUM('standard', 'important', 'urgent') DEFAULT 'important';

-- Verify the changes
SELECT priority, COUNT(*) as count 
FROM announcements 
GROUP BY priority;

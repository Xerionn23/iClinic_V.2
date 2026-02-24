-- Add section column to students table
ALTER TABLE students ADD COLUMN IF NOT EXISTS section VARCHAR(10) AFTER course;

-- Update students with sections based on their course
-- Each course will have 8 sections (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B)
-- Each section will have approximately 20 students

-- Computer Science students
SET @row_num = 0;
UPDATE students 
SET section = CASE 
    WHEN (@row_num := @row_num + 1) % 160 BETWEEN 0 AND 19 THEN '1A'
    WHEN (@row_num - 1) % 160 BETWEEN 20 AND 39 THEN '1B'
    WHEN (@row_num - 1) % 160 BETWEEN 40 AND 59 THEN '2A'
    WHEN (@row_num - 1) % 160 BETWEEN 60 AND 79 THEN '2B'
    WHEN (@row_num - 1) % 160 BETWEEN 80 AND 99 THEN '3A'
    WHEN (@row_num - 1) % 160 BETWEEN 100 AND 119 THEN '3B'
    WHEN (@row_num - 1) % 160 BETWEEN 120 AND 139 THEN '4A'
    ELSE '4B'
END
WHERE course = 'Computer Science';

-- BSED students
SET @row_num = 0;
UPDATE students 
SET section = CASE 
    WHEN (@row_num := @row_num + 1) % 160 BETWEEN 0 AND 19 THEN '1A'
    WHEN (@row_num - 1) % 160 BETWEEN 20 AND 39 THEN '1B'
    WHEN (@row_num - 1) % 160 BETWEEN 40 AND 59 THEN '2A'
    WHEN (@row_num - 1) % 160 BETWEEN 60 AND 79 THEN '2B'
    WHEN (@row_num - 1) % 160 BETWEEN 80 AND 99 THEN '3A'
    WHEN (@row_num - 1) % 160 BETWEEN 100 AND 119 THEN '3B'
    WHEN (@row_num - 1) % 160 BETWEEN 120 AND 139 THEN '4A'
    ELSE '4B'
END
WHERE course = 'BSED';

-- BEED students
SET @row_num = 0;
UPDATE students 
SET section = CASE 
    WHEN (@row_num := @row_num + 1) % 160 BETWEEN 0 AND 19 THEN '1A'
    WHEN (@row_num - 1) % 160 BETWEEN 20 AND 39 THEN '1B'
    WHEN (@row_num - 1) % 160 BETWEEN 40 AND 59 THEN '2A'
    WHEN (@row_num - 1) % 160 BETWEEN 60 AND 79 THEN '2B'
    WHEN (@row_num - 1) % 160 BETWEEN 80 AND 99 THEN '3A'
    WHEN (@row_num - 1) % 160 BETWEEN 100 AND 119 THEN '3B'
    WHEN (@row_num - 1) % 160 BETWEEN 120 AND 139 THEN '4A'
    ELSE '4B'
END
WHERE course = 'BEED';

-- HM (Hospitality Management) students
SET @row_num = 0;
UPDATE students 
SET section = CASE 
    WHEN (@row_num := @row_num + 1) % 160 BETWEEN 0 AND 19 THEN '1A'
    WHEN (@row_num - 1) % 160 BETWEEN 20 AND 39 THEN '1B'
    WHEN (@row_num - 1) % 160 BETWEEN 40 AND 59 THEN '2A'
    WHEN (@row_num - 1) % 160 BETWEEN 60 AND 79 THEN '2B'
    WHEN (@row_num - 1) % 160 BETWEEN 80 AND 99 THEN '3A'
    WHEN (@row_num - 1) % 160 BETWEEN 100 AND 119 THEN '3B'
    WHEN (@row_num - 1) % 160 BETWEEN 120 AND 139 THEN '4A'
    ELSE '4B'
END
WHERE course = 'HM';

-- Repeat for all other courses in your database
-- You can add more UPDATE statements for other courses following the same pattern

-- Verify the distribution
SELECT course, section, COUNT(*) as student_count
FROM students
WHERE section IS NOT NULL
GROUP BY course, section
ORDER BY course, section;

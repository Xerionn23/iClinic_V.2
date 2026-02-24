-- Insert Rotcher A. Cadorna Jr. into the database
-- Date: 2025-10-28

INSERT INTO students (
    student_number,
    std_Firstname,
    std_Surname,
    std_EmailAdd,
    std_ContactNum,
    std_Birthdate,
    std_Gender,
    std_Address,
    std_Course,
    std_Level,
    std_Curriculum,
    blood_type,
    emergency_contact_name,
    emergency_contact_number,
    medical_conditions,
    allergies
) VALUES (
    '2022-0186',
    'Rotcher A.',
    'Cadorna Jr.',
    'rotchercadorna123@gmail.com',
    '09123456789',
    '2003-05-15',
    'Male',
    'Tacloban City, Leyte',
    'Bachelor of Science in Information Technology',
    '3rd Year',
    '2022',
    'O+',
    'Maria Cadorna',
    '09187654321',
    'None',
    'None'
);

-- Verify the insertion
SELECT 
    student_number,
    CONCAT(std_Firstname, ' ', std_Surname) AS full_name,
    std_EmailAdd,
    std_Course,
    std_Level
FROM students 
WHERE student_number = '2022-0186';

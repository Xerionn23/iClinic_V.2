-- CORRECT SQL INSERT for Students
-- Using actual column names from students table (std_* prefix)

-- Student 1: Mary Joyce Pineda
INSERT INTO students (
    student_number,
    std_Firstname,
    std_Surname,
    std_Middlename,
    std_Gender,
    std_Birthdate,
    std_Age,
    std_EmailAdd,
    std_ContactNum,
    std_Course,
    std_Curriculum,
    std_Level,
    std_Status,
    is_active
) VALUES (
    '2022-0201',
    'Mary Joyce',
    'Pineda',
    'Catahan',
    'Female',
    '2002-03-12',
    19,
    'maryjoycepineda7@gmail.com',
    '09123456701',
    'Bachelor of Science in Computer Science',
    '2022',
    '3rd Year',
    'Active',
    TRUE
);

-- Student 2: Nizaniel Kate Lamadora
INSERT INTO students (
    student_number,
    std_Firstname,
    std_Surname,
    std_Middlename,
    std_Gender,
    std_Birthdate,
    std_Age,
    std_EmailAdd,
    std_ContactNum,
    std_Course,
    std_Curriculum,
    std_Level,
    std_Status,
    is_active
) VALUES (
    '2022-0220',
    'Nizaniel Kate',
    'Lamadora',
    'Ariaso',
    'Female',
    '2003-10-01',
    18,
    'nizanielkatelamadora@gmail.com',
    '09234567802',
    'Bachelor of Science in Computer Science',
    '2022',
    '3rd Year',
    'Active',
    TRUE
);

-- Student 3: Jeniebeth Sopeña
INSERT INTO students (
    student_number,
    std_Firstname,
    std_Surname,
    std_Middlename,
    std_Gender,
    std_Birthdate,
    std_Age,
    std_EmailAdd,
    std_ContactNum,
    std_Course,
    std_Curriculum,
    std_Level,
    std_Status,
    is_active
) VALUES (
    '2022-0516',
    'Jeniebeth',
    'Sopeña',
    'Solano',
    'Female',
    '2002-03-28',
    16,
    'jenibethsolano84@gmail.com',
    '09345678903',
    'Bachelor of Science in Computer Science',
    '2022',
    '3rd Year',
    'Active',
    TRUE
);

-- Verify insertion
SELECT 
    student_number,
    std_Firstname,
    std_Surname,
    std_Middlename,
    std_Gender,
    std_Age,
    std_EmailAdd,
    std_Course,
    std_Level
FROM students 
WHERE student_number IN ('2022-0201', '2022-0220', '2022-0516')
ORDER BY student_number;

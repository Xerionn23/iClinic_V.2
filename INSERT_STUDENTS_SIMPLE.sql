-- Simplified SQL INSERT for Students
-- Use this if the full version has errors

-- Student 1: Mary Joyce Pineda
INSERT INTO students (
    student_number, last_name, first_name, middle_name, gender, 
    date_of_birth, age, email, mobile_no, course, curriculum, 
    level, department, is_active
) VALUES (
    '2022-0201', 'Pineda', 'Mary Joyce', 'Catahan', 'Female',
    '2002-03-12', 19, 'maryjoycepineda7@gmail.com', '09123456701',
    'Bachelor of Science in Computer Science', '2022', '3rd Year',
    'College of Computer Studies', TRUE
);

-- Student 2: Nizaniel Kate Lamadora
INSERT INTO students (
    student_number, last_name, first_name, middle_name, gender,
    date_of_birth, age, email, mobile_no, course, curriculum,
    level, department, is_active
) VALUES (
    '2022-0220', 'Lamadora', 'Nizaniel Kate', 'Ariaso', 'Female',
    '2003-10-01', 18, 'nizanielkatelamadora@gmail.com', '09234567802',
    'Bachelor of Science in Computer Science', '2022', '3rd Year',
    'College of Computer Studies', TRUE
);

-- Student 3: Jeniebeth Sopeña
INSERT INTO students (
    student_number, last_name, first_name, middle_name, gender,
    date_of_birth, age, email, mobile_no, course, curriculum,
    level, department, is_active
) VALUES (
    '2022-0516', 'Sopeña', 'Jeniebeth', 'Solano', 'Female',
    '2002-03-28', 16, 'jenibethsolano84@gmail.com', '09345678903',
    'Bachelor of Science in Computer Science', '2022', '3rd Year',
    'College of Computer Studies', TRUE
);

-- Verify insertion
SELECT student_number, first_name, last_name, email, course, level
FROM students 
WHERE student_number IN ('2022-0201', '2022-0220', '2022-0516');

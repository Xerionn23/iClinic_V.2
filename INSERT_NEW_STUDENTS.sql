-- SQL INSERT Queries for New Students
-- Database: iclini_db
-- Table: students

-- Student 1: Mary Joyce Pineda
INSERT INTO students (
    student_status,
    picture,
    student_number,
    lrn,
    last_name,
    first_name,
    middle_name,
    suffix,
    gender,
    date_of_birth,
    place_of_birth,
    age,
    nationality,
    religion,
    province,
    city_municipality,
    barangay,
    house_street,
    email,
    mobile_no,
    father_last_name,
    father_first_name,
    father_email,
    father_mobile,
    mother_last_name,
    mother_first_name,
    mother_email,
    mother_mobile,
    course,
    curriculum,
    level,
    graduating,
    department,
    is_active
) VALUES (
    'Active',                           -- student_status
    'default-avatar.png',               -- picture
    '2022-0201',                        -- student_number
    '123456789012',                     -- lrn (12-digit Learner Reference Number)
    'Pineda',                           -- last_name
    'Mary Joyce',                       -- first_name
    'Catahan',                          -- middle_name
    '',                                 -- suffix (empty string instead of NULL)
    'Female',                           -- gender
    '2002-03-12',                       -- date_of_birth (YYYY-MM-DD format)
    'Norzagaray, Bulacan',             -- place_of_birth
    19,                                 -- age
    'Filipino',                         -- nationality
    'Roman Catholic',                   -- religion
    'Bulacan',                          -- province
    'Norzagaray',                       -- city_municipality
    'Poblacion',                        -- barangay
    'Purok 3, Poblacion',              -- house_street
    'maryjoycepineda7@gmail.com',      -- email
    '09123456701',                      -- mobile_no
    'Pineda',                           -- father_last_name
    'Roberto',                          -- father_first_name
    'roberto.pineda@gmail.com',         -- father_email
    '09171234501',                      -- father_mobile
    'Catahan',                          -- mother_last_name
    'Maria',                            -- mother_first_name
    'maria.catahan@gmail.com',          -- mother_email
    '09181234501',                      -- mother_mobile
    'Bachelor of Science in Computer Science', -- course
    '2022',                             -- curriculum
    '3rd Year',                         -- level
    'No',                               -- graduating
    'College of Computer Studies',     -- department
    TRUE                                -- is_active
);

-- Student 2: Nizaniel Kate Lamadora
INSERT INTO students (
    student_status,
    picture,
    student_number,
    lrn,
    last_name,
    first_name,
    middle_name,
    suffix,
    gender,
    date_of_birth,
    place_of_birth,
    age,
    nationality,
    religion,
    province,
    city_municipality,
    barangay,
    house_street,
    email,
    mobile_no,
    father_last_name,
    father_first_name,
    father_email,
    father_mobile,
    mother_last_name,
    mother_first_name,
    mother_email,
    mother_mobile,
    course,
    curriculum,
    level,
    graduating,
    department,
    is_active
) VALUES (
    'Active',                           -- student_status
    'default-avatar.png',               -- picture
    '2022-0220',                        -- student_number
    '123456789013',                     -- lrn (12-digit Learner Reference Number)
    'Lamadora',                         -- last_name
    'Nizaniel Kate',                    -- first_name
    'Ariaso',                           -- middle_name
    '',                                 -- suffix (empty string instead of NULL)
    'Female',                           -- gender
    '2003-10-01',                       -- date_of_birth (YYYY-MM-DD format)
    'Norzagaray, Bulacan',             -- place_of_birth
    18,                                 -- age
    'Filipino',                         -- nationality
    'Roman Catholic',                   -- religion
    'Bulacan',                          -- province
    'Norzagaray',                       -- city_municipality
    'San Lorenzo',                      -- barangay
    'Sitio Maligaya, San Lorenzo',     -- house_street
    'nizanielkatelamadora@gmail.com',  -- email
    '09234567802',                      -- mobile_no
    'Lamadora',                         -- father_last_name
    'Eduardo',                          -- father_first_name
    'eduardo.lamadora@gmail.com',       -- father_email
    '09172345602',                      -- father_mobile
    'Ariaso',                           -- mother_last_name
    'Catherine',                        -- mother_first_name
    'catherine.ariaso@gmail.com',       -- mother_email
    '09182345602',                      -- mother_mobile
    'Bachelor of Science in Computer Science', -- course
    '2022',                             -- curriculum
    '3rd Year',                         -- level
    'No',                               -- graduating
    'College of Computer Studies',     -- department
    TRUE                                -- is_active
);

-- Student 3: Jeniebeth Sopeña
INSERT INTO students (
    student_status,
    picture,
    student_number,
    lrn,
    last_name,
    first_name,
    middle_name,
    suffix,
    gender,
    date_of_birth,
    place_of_birth,
    age,
    nationality,
    religion,
    province,
    city_municipality,
    barangay,
    house_street,
    email,
    mobile_no,
    father_last_name,
    father_first_name,
    father_email,
    father_mobile,
    mother_last_name,
    mother_first_name,
    mother_email,
    mother_mobile,
    course,
    curriculum,
    level,
    graduating,
    department,
    is_active
) VALUES (
    'Active',                           -- student_status
    'default-avatar.png',               -- picture
    '2022-0516',                        -- student_number
    '123456789014',                     -- lrn (12-digit Learner Reference Number)
    'Sopeña',                           -- last_name
    'Jeniebeth',                        -- first_name
    'Solano',                           -- middle_name
    '',                                 -- suffix (empty string instead of NULL)
    'Female',                           -- gender
    '2002-03-28',                       -- date_of_birth (YYYY-MM-DD format)
    'Norzagaray, Bulacan',             -- place_of_birth
    16,                                 -- age
    'Filipino',                         -- nationality
    'Roman Catholic',                   -- religion
    'Bulacan',                          -- province
    'Norzagaray',                       -- city_municipality
    'Tigbe',                            -- barangay
    'Purok 5, Tigbe',                  -- house_street
    'jenibethsolano84@gmail.com',      -- email
    '09345678903',                      -- mobile_no
    'Sopeña',                           -- father_last_name
    'Fernando',                         -- father_first_name
    'fernando.sopena@gmail.com',        -- father_email
    '09173456703',                      -- father_mobile
    'Solano',                           -- mother_last_name
    'Rosario',                          -- mother_first_name
    'rosario.solano@gmail.com',         -- mother_email
    '09183456703',                      -- mother_mobile
    'Bachelor of Science in Computer Science', -- course
    '2022',                             -- curriculum
    '3rd Year',                         -- level
    'No',                               -- graduating
    'College of Computer Studies',     -- department
    TRUE                                -- is_active
);

-- Verification Query: Check if students were inserted successfully
SELECT 
    student_number,
    first_name,
    last_name,
    middle_name,
    gender,
    date_of_birth,
    age,
    email,
    course,
    level
FROM students 
WHERE student_number IN ('2022-0201', '2022-0220', '2022-0516')
ORDER BY student_number;

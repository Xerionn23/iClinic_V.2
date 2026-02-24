from config.database import DatabaseConfig

conn = DatabaseConfig.get_connection()
cursor = conn.cursor()

# Find students with user accounts
cursor.execute('''
    SELECT s.student_number, s.std_Firstname, s.std_Surname, u.email 
    FROM students s 
    INNER JOIN users u ON s.std_EmailAdd = u.email 
    WHERE u.role = 'student'
    LIMIT 5
''')

students_with_accounts = cursor.fetchall()
print('✅ Students with user accounts (can use forgot password):')
print('=' * 70)
for student in students_with_accounts:
    print(f'User ID: {student[0]} | Name: {student[1]} {student[2]} | Email: {student[3]}')

cursor.close()
conn.close()

from config.database import DatabaseConfig

conn = DatabaseConfig.get_connection()
cursor = conn.cursor()

# Get users without user_id
cursor.execute('SELECT id, email, role FROM users WHERE user_id IS NULL')
users = cursor.fetchall()

print("=" * 70)
print("USERS WITHOUT USER_ID:")
print("=" * 70)

for user in users:
    user_id, email, role = user
    print(f"\n👤 User ID: {user_id} | Email: {email} | Role: {role}")
    
    # Check if email exists in respective tables
    if role == 'staff':
        cursor.execute('SELECT nurse_id FROM nurses WHERE email = %s', (email,))
        nurse = cursor.fetchone()
        if nurse:
            print(f"   ✅ Found in nurses table: {nurse[0]}")
        else:
            print(f"   ❌ NOT found in nurses table")
    
    elif role == 'student':
        cursor.execute('SELECT student_number FROM students WHERE std_EmailAdd = %s', (email,))
        student = cursor.fetchone()
        if student:
            print(f"   ✅ Found in students table: {student[0]}")
        else:
            print(f"   ❌ NOT found in students table")
            # Try to find by partial match
            cursor.execute('SELECT student_number, std_EmailAdd FROM students WHERE std_EmailAdd LIKE %s LIMIT 3', (f'%{email.split("@")[0]}%',))
            matches = cursor.fetchall()
            if matches:
                print(f"   🔍 Similar emails found:")
                for match in matches:
                    print(f"      - {match[0]}: {match[1]}")

cursor.close()
conn.close()

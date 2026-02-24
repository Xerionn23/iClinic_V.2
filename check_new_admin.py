"""
Quick check for the newly created admin account
"""
import mysql.connector
from config.database import DatabaseConfig

conn = DatabaseConfig.get_connection()
cursor = conn.cursor()

# Show all users created in the last hour
print("\n📋 Recent user accounts (last 10):")
cursor.execute('''
    SELECT id, user_id, username, email, role, first_name, last_name, created_at 
    FROM users 
    ORDER BY created_at DESC
    LIMIT 10
''')

users = cursor.fetchall()
for user in users:
    print(f"\nID: {user[0]}")
    print(f"User ID: {user[1]}")
    print(f"Email: {user[3]}")
    print(f"Role: {user[4]}")
    print(f"Name: {user[5]} {user[6]}")
    print(f"Created: {user[7]}")

# Show all admins table entries
print("\n\n📋 All admins in admins table:")
cursor.execute('SELECT admin_id, first_name, last_name, email, status FROM admins')
admins = cursor.fetchall()
for admin in admins:
    print(f"Admin ID: {admin[0]}, Name: {admin[1]} {admin[2]}, Email: {admin[3]}, Status: {admin[4]}")

cursor.close()
conn.close()

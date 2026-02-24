"""
Quick script to check and fix user_id for FAC-CS-003
"""
import mysql.connector
from config.database import DatabaseConfig

def check_and_fix_user_id():
    """Check if FAC-CS-003 user has user_id populated"""
    
    conn = DatabaseConfig.get_connection()
    if not conn:
        print("❌ Database connection failed!")
        return
    
    cursor = conn.cursor()
    
    # Check if user exists with username FAC-CS-003
    print("\n🔍 Checking for user with username 'FAC-CS-003'...")
    cursor.execute('SELECT id, user_id, username, email, role, first_name, last_name FROM users WHERE username = %s', ('FAC-CS-003',))
    user = cursor.fetchone()
    
    if user:
        print(f"\n✅ Found user:")
        print(f"   ID: {user[0]}")
        print(f"   User ID: {user[1]}")
        print(f"   Username: {user[2]}")
        print(f"   Email: {user[3]}")
        print(f"   Role: {user[4]}")
        print(f"   Name: {user[5]} {user[6]}")
        
        if user[1] is None or user[1] == '':
            print(f"\n⚠️ User ID is empty! Fixing...")
            # Update user_id to match username
            cursor.execute('UPDATE users SET user_id = %s WHERE id = %s', (user[2], user[0]))
            conn.commit()
            print(f"✅ Updated user_id to: {user[2]}")
        else:
            print(f"\n✅ User ID is already set: {user[1]}")
    else:
        print("\n❌ User not found with username 'FAC-CS-003'")
        
        # Check if user exists with email
        print("\n🔍 Checking for user with email containing 'cadornajojo'...")
        cursor.execute('SELECT id, user_id, username, email, role, first_name, last_name FROM users WHERE email LIKE %s', ('%cadornajojo%',))
        user = cursor.fetchone()
        
        if user:
            print(f"\n✅ Found user by email:")
            print(f"   ID: {user[0]}")
            print(f"   User ID: {user[1]}")
            print(f"   Username: {user[2]}")
            print(f"   Email: {user[3]}")
            print(f"   Role: {user[4]}")
            print(f"   Name: {user[5]} {user[6]}")
            
            if user[1] is None or user[1] == '' or user[1] != 'FAC-CS-003':
                print(f"\n⚠️ User ID needs to be set to FAC-CS-003! Fixing...")
                cursor.execute('UPDATE users SET user_id = %s WHERE id = %s', ('FAC-CS-003', user[0]))
                conn.commit()
                print(f"✅ Updated user_id to: FAC-CS-003")
            else:
                print(f"\n✅ User ID is already correct: {user[1]}")
        else:
            print("\n❌ No user found with that email either")
    
    # Show all users for reference
    print("\n\n📋 All users in database:")
    cursor.execute('SELECT id, user_id, username, email, role FROM users LIMIT 10')
    users = cursor.fetchall()
    for u in users:
        print(f"   ID: {u[0]}, User ID: {u[1]}, Username: {u[2]}, Email: {u[3]}, Role: {u[4]}")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    check_and_fix_user_id()

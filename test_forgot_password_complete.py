"""
Complete test for forgot password functionality with user_id column
"""

from config.database import DatabaseConfig
import requests
import json

def test_forgot_password_system():
    """Test the complete forgot password system"""
    
    print("=" * 70)
    print("🧪 TESTING FORGOT PASSWORD SYSTEM WITH USER_ID COLUMN")
    print("=" * 70)
    print()
    
    # Step 1: Check if user_id column exists
    print("📋 Step 1: Checking if user_id column exists in users table...")
    conn = DatabaseConfig.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SHOW COLUMNS FROM users LIKE 'user_id'")
    if cursor.fetchone():
        print("✅ user_id column exists!")
    else:
        print("❌ user_id column NOT found!")
        return
    
    print()
    
    # Step 2: Check existing users
    print("📋 Step 2: Checking existing users...")
    cursor.execute('SELECT id, user_id, username, email, role FROM users LIMIT 5')
    users = cursor.fetchall()
    
    print(f"Found {len(users)} users:")
    print("-" * 70)
    for user in users:
        print(f"ID: {user[0]} | User ID: {user[1]} | Username: {user[2]} | Role: {user[4]}")
    print()
    
    # Step 3: Test forgot password with existing user
    print("📋 Step 3: Testing forgot password API...")
    
    # Find a user with user_id
    test_user = None
    for user in users:
        if user[1]:  # Has user_id
            test_user = user
            break
    
    if not test_user:
        print("⚠️  No users with user_id found. Creating test user...")
        
        # Create a test user with user_id
        cursor.execute('''
            INSERT INTO users (user_id, username, email, password_hash, role, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', ('TEST-001', 'test@test.com', 'test@test.com', 'dummy_hash', 'staff', 'Test', 'User'))
        conn.commit()
        
        test_user = ('TEST-001', 'test@test.com', 'test@test.com', 'dummy_hash', 'staff')
        print(f"✅ Created test user with User ID: TEST-001")
    
    print(f"Testing with User ID: {test_user[1]}")
    print()
    
    # Test API call
    try:
        response = requests.post(
            'http://127.0.0.1:5000/forgot-password',
            headers={'Content-Type': 'application/json'},
            json={'userId': test_user[1]}
        )
        
        print(f"API Response Status: {response.status_code}")
        print(f"API Response: {response.json()}")
        print()
        
        if response.status_code == 200:
            print("✅ FORGOT PASSWORD WORKING!")
            print("✅ User ID column successfully integrated!")
        else:
            print("❌ Forgot password failed")
            print(f"Error: {response.json().get('message')}")
    
    except Exception as e:
        print(f"❌ API call failed: {e}")
    
    cursor.close()
    conn.close()
    
    print()
    print("=" * 70)
    print("🎉 TEST COMPLETED!")
    print("=" * 70)

if __name__ == '__main__':
    test_forgot_password_system()

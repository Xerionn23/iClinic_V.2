import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'iclinic_db'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    emails = ['maryjoycepineda7@gmail.com', 'nizanielkatelamadora@gmail.com']
    
    print("\n" + "="*80)
    print("📋 CURRENT USER INFORMATION")
    print("="*80)
    
    for email in emails:
        cursor.execute("""
            SELECT id, user_id, username, email, first_name, last_name, 
                   role, position, created_at 
            FROM users 
            WHERE email = %s
        """, (email,))
        
        user = cursor.fetchone()
        
        if user:
            print(f"\n👤 {user['first_name']} {user['last_name']}")
            print(f"   📧 Email: {user['email']}")
            print(f"   🆔 Database ID: {user['id']}")
            print(f"   🆔 User ID: {user.get('user_id', 'N/A')}")
            print(f"   👤 Username: {user['username']}")
            print(f"   📝 Role: {user['role']}")
            print(f"   💼 Position: {user['position']}")
            print(f"   📅 Created: {user['created_at']}")
        else:
            print(f"\n❌ User not found: {email}")
    
    print("\n" + "="*80)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

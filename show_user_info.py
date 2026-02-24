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
    
    print("\n" + "="*100)
    print("CURRENT USER INFORMATION")
    print("="*100)
    
    # Mary Joyce Pineda
    cursor.execute("SELECT * FROM users WHERE email = 'maryjoycepineda7@gmail.com'")
    user1 = cursor.fetchone()
    
    if user1:
        print("\n1. MARY JOYCE PINEDA (Teaching Staff)")
        print(f"   Email: {user1['email']}")
        print(f"   User ID (Database): {user1['id']}")
        print(f"   Username: {user1['username']}")
        print(f"   Role: {user1['role']}")
        print(f"   Position: {user1['position']}")
    
    # Nizaniel Kate Lamadora
    cursor.execute("SELECT * FROM users WHERE email = 'nizanielkatelamadora@gmail.com'")
    user2 = cursor.fetchone()
    
    if user2:
        print("\n2. NIZANIEL KATE LAMADORA (Dean)")
        print(f"   Email: {user2['email']}")
        print(f"   User ID (Database): {user2['id']}")
        print(f"   Username: {user2['username']}")
        print(f"   Role: {user2['role']}")
        print(f"   Position: {user2['position']}")
    
    print("\n" + "="*100)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")

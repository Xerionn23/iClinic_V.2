import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'iclinic_db'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    print("Checking users table...")
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    
    print("\nUsers table columns:")
    print("="*80)
    for col in columns:
        print(f"{col[0]:30} {col[1]:30} {col[2]}")
    print("="*80)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

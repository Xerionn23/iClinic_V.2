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
    
    cursor.execute("DESCRIBE students")
    columns = cursor.fetchall()
    
    print("Students table columns:")
    print("="*60)
    for col in columns:
        print(f"{col[0]:30} {col[1]:20} {col[2]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")

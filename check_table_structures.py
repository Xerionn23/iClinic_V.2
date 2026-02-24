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
    
    print("\n" + "="*80)
    print("DEANS TABLE STRUCTURE")
    print("="*80)
    cursor.execute("DESCRIBE deans")
    for col in cursor.fetchall():
        print(f"{col[0]:30} {col[1]:30}")
    
    print("\n" + "="*80)
    print("TEACHING TABLE STRUCTURE")
    print("="*80)
    cursor.execute("DESCRIBE teaching")
    for col in cursor.fetchall():
        print(f"{col[0]:30} {col[1]:30}")
    
    print("\n" + "="*80)
    print("CURRENT DATA IN DEANS TABLE")
    print("="*80)
    cursor.execute("SELECT * FROM deans")
    deans = cursor.fetchall()
    print(f"Total records: {len(deans)}")
    
    print("\n" + "="*80)
    print("CURRENT DATA IN TEACHING TABLE")
    print("="*80)
    cursor.execute("SELECT * FROM teaching")
    teaching = cursor.fetchall()
    print(f"Total records: {len(teaching)}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

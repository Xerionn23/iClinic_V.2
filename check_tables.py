import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='iclinic_db'
    )
    cursor = conn.cursor()
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print('\n' + '='*70)
    print('📋 ALL TABLES IN iclinic_db DATABASE:')
    print('='*70)
    
    for i, (table,) in enumerate(tables, 1):
        print(f'{i:3}. {table}')
    
    print('='*70)
    print(f'Total tables: {len(tables)}')
    print('='*70)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'❌ Error: {e}')

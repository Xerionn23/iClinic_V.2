import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='iclinic_db'
    )
    cursor = conn.cursor()
    
    tables = [
        ('teaching', 'Teaching Staff'),
        ('non_teaching_staff', 'Non-Teaching Staff'),
        ('deans', 'Deans'),
        ('president', 'President'),
        ('visitors', 'Visitors')
    ]
    
    print('\n' + '='*70)
    print('📋 CHECKING COLUMN NAMES IN EACH TABLE')
    print('='*70)
    
    for table_name, label in tables:
        print(f'\n🔍 {label} ({table_name}):')
        try:
            cursor.execute(f'DESCRIBE {table_name}')
            columns = cursor.fetchall()
            print(f'   Columns: {", ".join([col[0] for col in columns])}')
        except Exception as e:
            print(f'   ❌ Error: {e}')
    
    print('\n' + '='*70)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'❌ Error: {e}')

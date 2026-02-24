import mysql.connector

try:
    # Connect to database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='iclinic_db'
    )
    cursor = conn.cursor()
    
    # List of medical records tables
    tables = [
        ('medical_records', 'Students'),
        ('teaching_medical_records', 'Teaching Staff'),
        ('non_teaching_medical_records', 'Non-Teaching Staff'),
        ('dean_medical_records', 'Dean'),
        ('president_medical_records', 'President'),
        ('visitor_medical_records', 'Visitors')
    ]
    
    print('\n' + '='*70)
    print('📊 MEDICAL RECORDS COUNT PER TABLE')
    print('='*70)
    print(f'{"Patient Type":<30} | {"Table Name":<35} | {"Count":>5}')
    print('-'*70)
    
    total = 0
    for table_name, patient_type in tables:
        try:
            cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
            count = cursor.fetchone()[0]
            total += count
            status = '✅' if count > 0 else '⚠️'
            print(f'{status} {patient_type:<27} | {table_name:<35} | {count:>5}')
        except Exception as e:
            print(f'❌ {patient_type:<27} | {table_name:<35} | ERROR')
    
    print('-'*70)
    print(f'{"TOTAL MEDICAL RECORDS":<30} | {"ALL TABLES":<35} | {total:>5}')
    print('='*70)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'❌ Database connection error: {e}')

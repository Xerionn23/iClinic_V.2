import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='iclinic_db'
    )
    cursor = conn.cursor()
    
    print('\n' + '='*70)
    print('🔍 DEBUGGING VISITS API - CHECKING EACH QUERY')
    print('='*70)
    
    # 1. Students
    print('\n1️⃣ STUDENTS (medical_records):')
    cursor.execute('SELECT COUNT(*) FROM medical_records')
    total = cursor.fetchone()[0]
    cursor.execute('''
        SELECT COUNT(*) 
        FROM medical_records mr
        INNER JOIN students s ON mr.student_number = s.student_number
    ''')
    joined = cursor.fetchone()[0]
    print(f'   Total in medical_records: {total}')
    print(f'   After INNER JOIN: {joined}')
    print(f'   ❌ Missing: {total - joined}')
    
    # 2. Teaching Staff
    print('\n2️⃣ TEACHING STAFF (teaching_medical_records):')
    cursor.execute('SELECT COUNT(*) FROM teaching_medical_records')
    total = cursor.fetchone()[0]
    cursor.execute('''
        SELECT COUNT(*) 
        FROM teaching_medical_records tmr
        INNER JOIN teaching_staff ts ON tmr.teaching_staff_id = ts.id
    ''')
    joined = cursor.fetchone()[0]
    print(f'   Total in teaching_medical_records: {total}')
    print(f'   After INNER JOIN: {joined}')
    print(f'   ❌ Missing: {total - joined}')
    
    # 3. Non-Teaching Staff
    print('\n3️⃣ NON-TEACHING STAFF (non_teaching_medical_records):')
    cursor.execute('SELECT COUNT(*) FROM non_teaching_medical_records')
    total = cursor.fetchone()[0]
    cursor.execute('''
        SELECT COUNT(*) 
        FROM non_teaching_medical_records ntmr
        INNER JOIN non_teaching_staff nts ON ntmr.non_teaching_staff_id = nts.id
    ''')
    joined = cursor.fetchone()[0]
    print(f'   Total in non_teaching_medical_records: {total}')
    print(f'   After INNER JOIN: {joined}')
    print(f'   ❌ Missing: {total - joined}')
    
    # 4. Dean
    print('\n4️⃣ DEAN (dean_medical_records):')
    cursor.execute('SELECT COUNT(*) FROM dean_medical_records')
    total = cursor.fetchone()[0]
    print(f'   Total in dean_medical_records: {total}')
    
    # 5. President
    print('\n5️⃣ PRESIDENT (president_medical_records):')
    cursor.execute('SELECT COUNT(*) FROM president_medical_records')
    total = cursor.fetchone()[0]
    cursor.execute('''
        SELECT COUNT(*) 
        FROM president_medical_records pmr
        INNER JOIN president p ON pmr.president_id = p.id
    ''')
    joined = cursor.fetchone()[0]
    print(f'   Total in president_medical_records: {total}')
    print(f'   After INNER JOIN: {joined}')
    print(f'   ❌ Missing: {total - joined}')
    
    # 6. Visitors
    print('\n6️⃣ VISITORS (visitor_medical_records):')
    cursor.execute('SELECT COUNT(*) FROM visitor_medical_records')
    total = cursor.fetchone()[0]
    cursor.execute('''
        SELECT COUNT(*) 
        FROM visitor_medical_records vmr
        INNER JOIN visitors v ON vmr.visitor_id = v.id
    ''')
    joined = cursor.fetchone()[0]
    print(f'   Total in visitor_medical_records: {total}')
    print(f'   After INNER JOIN: {joined}')
    print(f'   ❌ Missing: {total - joined}')
    
    print('\n' + '='*70)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()

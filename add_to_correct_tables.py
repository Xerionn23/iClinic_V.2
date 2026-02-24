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
    
    print("\n" + "="*80)
    print("ADDING USERS TO CORRECT TABLES")
    print("="*80)
    
    # 1. Add Mary Joyce Pineda to teaching table
    print("\n1️⃣ Adding Mary Joyce Pineda to TEACHING table...")
    
    # Check structure first
    cursor.execute("DESCRIBE teaching")
    cols = cursor.fetchall()
    teaching_cols = [col['Field'] for col in cols]
    print(f"   Teaching table columns: {', '.join(teaching_cols[:5])}...")
    
    # Get next faculty_id
    cursor.execute("SELECT MAX(CAST(SUBSTRING(faculty_id, 8) AS UNSIGNED)) as max_id FROM teaching WHERE faculty_id LIKE 'FAC-CS-%'")
    result = cursor.fetchone()
    next_num = (result['max_id'] or 0) + 1
    faculty_id = f"FAC-CS-{str(next_num).zfill(3)}"
    
    # Get next faculty_number
    cursor.execute("SELECT MAX(faculty_number) as max_num FROM teaching")
    result = cursor.fetchone()
    next_faculty_num = int(result['max_num'] or 1000) + 1
    
    cursor.execute("""
        INSERT INTO teaching (
            faculty_id, faculty_number, first_name, last_name, email,
            rank, hire_date, specialization, is_archived, created_at, updated_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s, NOW(), %s, 0, NOW(), NOW()
        )
    """, (
        faculty_id,
        next_faculty_num,
        'Mary Joyce',
        'Pineda',
        'maryjoycepineda7@gmail.com',
        'Professor',
        'Education'
    ))
    conn.commit()
    print(f"   ✅ Added to teaching table with Faculty ID: {faculty_id}")
    
    # 2. Add Nizaniel Kate Lamadora to deans table
    print("\n2️⃣ Adding Nizaniel Kate Lamadora to DEANS table...")
    
    # Check structure first
    cursor.execute("DESCRIBE deans")
    cols = cursor.fetchall()
    deans_cols = [col['Field'] for col in cols]
    print(f"   Deans table columns: {', '.join(deans_cols[:5])}...")
    
    # Get next dean_id
    cursor.execute("SELECT MAX(CAST(SUBSTRING(dean_id, 6) AS UNSIGNED)) as max_id FROM deans WHERE dean_id LIKE 'DEAN-%'")
    result = cursor.fetchone()
    next_num = (result['max_id'] or 0) + 1
    dean_id = f"DEAN-{str(next_num).zfill(3)}"
    
    # Get next employee_number
    cursor.execute("SELECT MAX(SUBSTRING(employee_number, 13)) as max_num FROM deans WHERE employee_number LIKE 'EMP-DEAN-%'")
    result = cursor.fetchone()
    if result['max_num']:
        next_emp_num = int(result['max_num']) + 1
    else:
        next_emp_num = 1
    employee_number = f"EMP-DEAN-{str(next_emp_num).zfill(3)}"
    
    cursor.execute("""
        INSERT INTO deans (
            dean_id, employee_number, first_name, last_name, email,
            college, department, status
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        dean_id,
        employee_number,
        'Nizaniel Kate',
        'Lamadora',
        'nizanielkatelamadora@gmail.com',
        'COLLEGE OF EDUCATION',
        'EDUC',
        'Active'
    ))
    conn.commit()
    print(f"   ✅ Added to deans table with Dean ID: {dean_id}")
    
    print("\n" + "="*80)
    print("✅ SUCCESSFULLY ADDED TO CORRECT TABLES")
    print("="*80)
    
    # Verify
    print("\n📋 VERIFICATION:")
    cursor.execute("SELECT * FROM teaching WHERE email = 'maryjoycepineda7@gmail.com'")
    teaching_user = cursor.fetchone()
    if teaching_user:
        print(f"\n✅ Mary Joyce Pineda in TEACHING table:")
        print(f"   Faculty ID: {teaching_user['faculty_id']}")
        print(f"   Faculty Number: {teaching_user['faculty_number']}")
        print(f"   Email: {teaching_user['email']}")
    
    cursor.execute("SELECT * FROM deans WHERE email = 'nizanielkatelamadora@gmail.com'")
    dean_user = cursor.fetchone()
    if dean_user:
        print(f"\n✅ Nizaniel Kate Lamadora in DEANS table:")
        print(f"   Dean ID: {dean_user['dean_id']}")
        print(f"   Employee Number: {dean_user['employee_number']}")
        print(f"   Email: {dean_user['email']}")
    
    print("\n" + "="*80)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

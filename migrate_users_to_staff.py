import mysql.connector
from datetime import datetime

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'iclinic_db'
}

def migrate_user_to_teaching_staff():
    """
    Migrate Mary Joyce Pineda from students to teaching staff
    """
    print("="*80)
    print("MIGRATING MARY JOYCE PINEDA TO TEACHING STAFF")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # User details
        email = 'maryjoycepineda7@gmail.com'
        student_number = '2022-0201'
        
        # Step 1: Check if user exists in students table
        print(f"\n1️⃣ Checking if {email} exists in students table...")
        cursor.execute("""
            SELECT * FROM students 
            WHERE std_EmailAdd = %s OR student_number = %s
        """, (email, student_number))
        
        student = cursor.fetchone()
        
        if student:
            print(f"   ✅ Found student: {student['std_Firstname']} {student['std_Surname']}")
            print(f"   📧 Email: {student['std_EmailAdd']}")
            print(f"   🆔 Student Number: {student.get('student_number', 'N/A')}")
            
            # Step 2: Delete from students table
            print(f"\n2️⃣ Deleting from students table...")
            cursor.execute("""
                DELETE FROM students 
                WHERE std_EmailAdd = %s OR student_number = %s
            """, (email, student_number))
            conn.commit()
            print(f"   ✅ Deleted successfully")
        else:
            print(f"   ℹ️ User not found in students table")
        
        # Step 3: Check if user already exists in users table
        print(f"\n3️⃣ Checking if {email} exists in users table...")
        cursor.execute("""
            SELECT * FROM users WHERE email = %s
        """, (email,))
        
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"   ⚠️ User already exists in users table with ID: {existing_user['id']}")
            print(f"   📝 Current role: {existing_user['role']}")
            print(f"   📝 Current position: {existing_user.get('position', 'N/A')}")
            
            # Update to teaching staff
            print(f"\n4️⃣ Updating user to teaching staff role...")
            cursor.execute("""
                UPDATE users 
                SET role = 'staff',
                    position = 'Teaching Staff',
                    updated_at = NOW()
                WHERE email = %s
            """, (email,))
            conn.commit()
            print(f"   ✅ Updated to Teaching Staff")
            
        else:
            # Step 4: Create new user in users table with teaching staff role
            print(f"\n4️⃣ Creating new user in users table as Teaching Staff...")
            
            # Generate new user ID for teaching staff (format: TS-XXXX)
            cursor.execute("""
                SELECT id FROM users 
                WHERE id LIKE 'TS-%' 
                ORDER BY id DESC LIMIT 1
            """)
            last_ts = cursor.fetchone()
            
            if last_ts:
                last_num = int(last_ts['id'].split('-')[1])
                new_id = f"TS-{str(last_num + 1).zfill(4)}"
            else:
                new_id = "TS-0001"
            
            print(f"   🆔 Generated User ID: {new_id}")
            
            # Insert new user
            cursor.execute("""
                INSERT INTO users (
                    id, username, email, first_name, last_name,
                    role, position, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, NOW()
                )
            """, (
                new_id,
                email.split('@')[0],  # username from email
                email,
                'Mary Joyce',
                'Pineda',
                'staff',
                'Teaching Staff'
            ))
            conn.commit()
            print(f"   ✅ Created new Teaching Staff user with ID: {new_id}")
        
        print("\n" + "="*80)
        print("✅ MARY JOYCE PINEDA MIGRATION COMPLETED")
        print("="*80)
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        try:
            if 'conn' in locals() and conn:
                conn.rollback()
        except:
            pass
    except Exception as e:
        print(f"❌ Error: {e}")


def migrate_user_to_dean():
    """
    Migrate Nizaniel Kate Lamadora to dean role
    """
    print("\n" + "="*80)
    print("MIGRATING NIZANIEL KATE LAMADORA TO DEAN")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # User details
        email = 'nizanielkatelamadora@gmail.com'
        student_number = '2022-0220'
        
        # Step 1: Check if user exists in students table
        print(f"\n1️⃣ Checking if {email} exists in students table...")
        cursor.execute("""
            SELECT * FROM students 
            WHERE std_EmailAdd = %s OR student_number = %s
        """, (email, student_number))
        
        student = cursor.fetchone()
        
        if student:
            print(f"   ✅ Found student: {student['std_Firstname']} {student['std_Surname']}")
            print(f"   📧 Email: {student['std_EmailAdd']}")
            print(f"   🆔 Student Number: {student.get('student_number', 'N/A')}")
            
            # Step 2: Delete from students table
            print(f"\n2️⃣ Deleting from students table...")
            cursor.execute("""
                DELETE FROM students 
                WHERE std_EmailAdd = %s OR student_number = %s
            """, (email, student_number))
            conn.commit()
            print(f"   ✅ Deleted successfully")
        else:
            print(f"   ℹ️ User not found in students table")
        
        # Step 3: Check if user already exists in users table
        print(f"\n3️⃣ Checking if {email} exists in users table...")
        cursor.execute("""
            SELECT * FROM users WHERE email = %s
        """, (email,))
        
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"   ⚠️ User already exists in users table with ID: {existing_user['id']}")
            print(f"   📝 Current role: {existing_user['role']}")
            print(f"   📝 Current position: {existing_user.get('position', 'N/A')}")
            
            # Generate new Dean ID
            print(f"\n4️⃣ Generating new Dean ID...")
            cursor.execute("""
                SELECT id FROM users 
                WHERE id LIKE 'DEAN-%' 
                ORDER BY id DESC LIMIT 1
            """)
            last_dean = cursor.fetchone()
            
            if last_dean:
                last_num = int(last_dean['id'].split('-')[1])
                new_id = f"DEAN-{str(last_num + 1).zfill(4)}"
            else:
                new_id = "DEAN-0001"
            
            print(f"   🆔 New Dean ID: {new_id}")
            
            # Update user with new ID and role
            print(f"\n5️⃣ Updating user to Dean role with new ID...")
            cursor.execute("""
                UPDATE users 
                SET id = %s,
                    role = 'dean',
                    position = 'Dean',
                    updated_at = NOW()
                WHERE email = %s
            """, (new_id, email))
            conn.commit()
            print(f"   ✅ Updated to Dean with ID: {new_id}")
            
        else:
            # Step 4: Create new user in users table with dean role
            print(f"\n4️⃣ Creating new user in users table as Dean...")
            
            # Generate new Dean ID
            cursor.execute("""
                SELECT id FROM users 
                WHERE id LIKE 'DEAN-%' 
                ORDER BY id DESC LIMIT 1
            """)
            last_dean = cursor.fetchone()
            
            if last_dean:
                last_num = int(last_dean['id'].split('-')[1])
                new_id = f"DEAN-{str(last_num + 1).zfill(4)}"
            else:
                new_id = "DEAN-0001"
            
            print(f"   🆔 Generated Dean ID: {new_id}")
            
            # Insert new user
            cursor.execute("""
                INSERT INTO users (
                    id, username, email, first_name, last_name,
                    role, position, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, NOW()
                )
            """, (
                new_id,
                email.split('@')[0],  # username from email
                email,
                'Nizaniel Kate',
                'Lamadora',
                'dean',
                'Dean'
            ))
            conn.commit()
            print(f"   ✅ Created new Dean user with ID: {new_id}")
        
        print("\n" + "="*80)
        print("✅ NIZANIEL KATE LAMADORA MIGRATION COMPLETED")
        print("="*80)
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        try:
            if 'conn' in locals() and conn:
                conn.rollback()
        except:
            pass
    except Exception as e:
        print(f"❌ Error: {e}")


def verify_migrations():
    """
    Verify that both users have been migrated successfully
    """
    print("\n" + "="*80)
    print("VERIFYING MIGRATIONS")
    print("="*80)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        emails = ['maryjoycepineda7@gmail.com', 'nizanielkatelamadora@gmail.com']
        
        for email in emails:
            print(f"\n📧 Checking {email}...")
            
            # Check students table
            cursor.execute("SELECT * FROM students WHERE std_EmailAdd = %s", (email,))
            student = cursor.fetchone()
            
            if student:
                print(f"   ⚠️ Still in students table: {student['std_Firstname']} {student['std_Surname']}")
            else:
                print(f"   ✅ Not in students table")
            
            # Check users table
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user:
                print(f"   ✅ Found in users table:")
                print(f"      🆔 ID: {user['id']}")
                print(f"      👤 Name: {user['first_name']} {user['last_name']}")
                print(f"      📝 Role: {user['role']}")
                print(f"      💼 Position: {user.get('position', 'N/A')}")
            else:
                print(f"   ❌ Not found in users table")
        
        print("\n" + "="*80)
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("\n🏥 iClinic User Migration Script")
    print("="*80)
    print("This script will migrate users from students to staff roles")
    print("="*80)
    
    # Migrate Mary Joyce Pineda to Teaching Staff
    migrate_user_to_teaching_staff()
    
    # Migrate Nizaniel Kate Lamadora to Dean
    migrate_user_to_dean()
    
    # Verify migrations
    verify_migrations()
    
    print("\n✅ All migrations completed!")
    print("="*80)

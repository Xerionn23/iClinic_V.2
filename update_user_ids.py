"""
Script to populate user_id column for existing users in the database
This will match users with their corresponding ID numbers from their respective tables
"""

from config.database import DatabaseConfig

def update_user_ids():
    """Update user_id column for all existing users"""
    conn = DatabaseConfig.get_connection()
    if not conn:
        print("❌ Failed to connect to database")
        return
    
    cursor = conn.cursor()
    
    try:
        # Get all users without user_id
        cursor.execute('SELECT id, email, role, username FROM users WHERE user_id IS NULL OR user_id = ""')
        users = cursor.fetchall()
        
        print(f"📊 Found {len(users)} users without user_id")
        print("=" * 70)
        
        updated_count = 0
        
        for user in users:
            user_db_id, email, role, username = user
            user_id_value = None
            
            # Try to find user_id based on role and email
            if role == 'student':
                cursor.execute('SELECT student_number FROM students WHERE std_EmailAdd = %s', (email,))
                result = cursor.fetchone()
                if result:
                    user_id_value = result[0]
                    print(f"✅ Student: {email} → User ID: {user_id_value}")
            
            elif role == 'staff':
                # Check if nurse
                cursor.execute('SELECT nurse_id FROM nurses WHERE email = %s', (email,))
                result = cursor.fetchone()
                if result:
                    user_id_value = result[0]
                    print(f"✅ Nurse: {email} → User ID: {user_id_value}")
                else:
                    # Check if admin
                    cursor.execute('SELECT admin_id FROM admins WHERE email = %s', (email,))
                    result = cursor.fetchone()
                    if result:
                        user_id_value = result[0]
                        print(f"✅ Admin: {email} → User ID: {user_id_value}")
            
            elif role == 'teaching_staff':
                cursor.execute('SELECT faculty_id FROM teaching WHERE email = %s', (email,))
                result = cursor.fetchone()
                if result:
                    user_id_value = result[0]
                    print(f"✅ Teaching Staff: {email} → User ID: {user_id_value}")
            
            elif role == 'non_teaching_staff':
                cursor.execute('SELECT staff_id FROM non_teaching_staff WHERE email = %s', (email,))
                result = cursor.fetchone()
                if result:
                    user_id_value = result[0]
                    print(f"✅ Non-Teaching Staff: {email} → User ID: {user_id_value}")
            
            elif role == 'president':
                cursor.execute('SELECT president_id FROM president WHERE email = %s', (email,))
                result = cursor.fetchone()
                if result:
                    user_id_value = result[0]
                    print(f"✅ President: {email} → User ID: {user_id_value}")
            
            elif role == 'deans':
                cursor.execute('SELECT dean_id FROM deans WHERE email = %s', (email,))
                result = cursor.fetchone()
                if result:
                    user_id_value = result[0]
                    print(f"✅ Dean: {email} → User ID: {user_id_value}")
            
            elif role == 'admin':
                # Use username as user_id for admin accounts
                user_id_value = username
                print(f"✅ Admin: {email} → User ID: {user_id_value}")
            
            # Update user_id if found
            if user_id_value:
                cursor.execute('UPDATE users SET user_id = %s WHERE id = %s', (user_id_value, user_db_id))
                updated_count += 1
            else:
                print(f"⚠️  Could not find user_id for: {email} (role: {role})")
        
        conn.commit()
        print("=" * 70)
        print(f"✅ Successfully updated {updated_count} users with user_id")
        
    except Exception as e:
        print(f"❌ Error updating user_ids: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("🔧 Starting user_id population script...")
    print()
    update_user_ids()
    print()
    print("✅ Script completed!")

"""
Fix the newly created admin account that doesn't have user_id populated
"""
import mysql.connector
from config.database import DatabaseConfig

def fix_new_admin():
    """Find and fix the newly created admin account"""
    
    conn = DatabaseConfig.get_connection()
    if not conn:
        print("❌ Database connection failed!")
        return
    
    cursor = conn.cursor()
    
    # Find the most recent admin account without user_id
    print("\n🔍 Looking for admin accounts without user_id...")
    cursor.execute('''
        SELECT id, username, email, role, first_name, last_name, created_at 
        FROM users 
        WHERE role = 'admin' AND (user_id IS NULL OR user_id = '')
        ORDER BY created_at DESC
        LIMIT 5
    ''')
    
    admins_without_id = cursor.fetchall()
    
    if not admins_without_id:
        print("✅ All admin accounts have user_id populated!")
        cursor.close()
        conn.close()
        return
    
    print(f"\n⚠️ Found {len(admins_without_id)} admin account(s) without user_id:\n")
    
    for admin in admins_without_id:
        admin_id, username, email, role, first_name, last_name, created_at = admin
        print(f"   ID: {admin_id}")
        print(f"   Email: {email}")
        print(f"   Name: {first_name} {last_name}")
        print(f"   Created: {created_at}")
        print()
    
    # Check admins table to find the correct admin_id
    print("🔍 Checking admins table for matching records...")
    
    for admin in admins_without_id:
        admin_id, username, email, role, first_name, last_name, created_at = admin
        
        # Try to find matching admin in admins table
        cursor.execute('''
            SELECT admin_id, first_name, last_name, email 
            FROM admins 
            WHERE email = %s OR CONCAT(first_name, ' ', last_name) = %s
        ''', (email, f"{first_name} {last_name}"))
        
        admin_record = cursor.fetchone()
        
        if admin_record:
            admin_id_from_table, fname, lname, admin_email = admin_record
            print(f"✅ Found matching admin in admins table:")
            print(f"   Admin ID: {admin_id_from_table}")
            print(f"   Name: {fname} {lname}")
            print(f"   Email: {admin_email}")
            
            # Update users table with correct user_id
            cursor.execute('''
                UPDATE users 
                SET user_id = %s 
                WHERE id = %s
            ''', (admin_id_from_table, admin_id))
            
            conn.commit()
            print(f"✅ Updated user_id to: {admin_id_from_table}\n")
        else:
            print(f"⚠️ No matching admin found in admins table for {email}")
            print(f"   Creating generic admin_id based on user ID...")
            
            # Generate admin_id based on database ID
            generated_admin_id = f"ADMIN-{admin_id:03d}"
            
            cursor.execute('''
                UPDATE users 
                SET user_id = %s 
                WHERE id = %s
            ''', (generated_admin_id, admin_id))
            
            conn.commit()
            print(f"✅ Updated user_id to: {generated_admin_id}\n")
    
    # Show all admin accounts now
    print("\n📋 All admin accounts after fix:")
    cursor.execute('''
        SELECT id, user_id, username, email, role, first_name, last_name 
        FROM users 
        WHERE role = 'admin'
        ORDER BY created_at DESC
    ''')
    
    all_admins = cursor.fetchall()
    for admin in all_admins:
        print(f"   ID: {admin[0]}, User ID: {admin[1]}, Email: {admin[3]}, Name: {admin[5]} {admin[6]}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Fix complete! You can now login with your User ID.")

if __name__ == '__main__':
    fix_new_admin()

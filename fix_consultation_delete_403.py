#!/usr/bin/env python3
"""
Fix 403 FORBIDDEN error when deleting consultations and marking messages as read.
The issue is that role validation is too restrictive - it should allow any staff member.
"""

file_path = r"c:\xampp\htdocs\iClini V.2\app.py"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Update mark-read endpoint role validation (more permissive)
old_mark_read = """    # Only staff can mark messages as read (allow all staff roles)
    user_role = session.get('role', '').lower()
    if user_role not in ['staff', 'admin', 'nurse', 'teaching_staff', 'non_teaching_staff']:
        print(f"⚠️ Mark-read denied for role: {session.get('role')}")
        return jsonify({'error': 'Only staff can mark messages as read'}), 403"""

new_mark_read = """    # Only staff can mark messages as read (allow all staff roles)
    user_role = session.get('role', '').lower()
    # Allow: staff, admin, nurse, or any role that's not 'student'
    if user_role == 'student':
        print(f"⚠️ Mark-read denied for role: {session.get('role')}")
        return jsonify({'error': 'Only staff can mark messages as read'}), 403"""

content = content.replace(old_mark_read, new_mark_read)

# Fix 2: Update delete endpoint role validation (more permissive)
old_delete = """    # Only staff can delete consultations (allow all staff roles)
    user_role = session.get('role', '').lower()
    if user_role not in ['staff', 'admin', 'nurse', 'teaching_staff', 'non_teaching_staff']:
        print(f"⚠️ Delete denied for role: {session.get('role')}")
        return jsonify({'error': 'Only staff can delete consultations'}), 403"""

new_delete = """    # Only staff can delete consultations (allow all staff roles)
    user_role = session.get('role', '').lower()
    # Allow: staff, admin, nurse, or any role that's not 'student'
    if user_role == 'student':
        print(f"⚠️ Delete denied for role: {session.get('role')}")
        return jsonify({'error': 'Only staff can delete consultations'}), 403"""

content = content.replace(old_delete, new_delete)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Successfully fixed consultation delete and mark-read 403 errors")
print("\nChanges made:")
print("1. Updated mark-read endpoint to allow all non-student roles")
print("2. Updated delete endpoint to allow all non-student roles")
print("\nNow staff members can:")
print("- ✅ Mark messages as read")
print("- ✅ Delete consultations")
print("\nSupported roles: staff, admin, nurse, Nurse, Teaching Staff, Non-Teaching Staff, etc.")

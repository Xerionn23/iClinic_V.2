#!/usr/bin/env python3
"""
Add debug logging to see what role is being checked
"""

file_path = r"c:\xampp\htdocs\iClini V.2\app.py"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add debug logging for mark-read endpoint
old_mark = """    # Only staff can mark messages as read (allow all staff roles)
    user_role = session.get('role', '').lower()
    # Allow: staff, admin, nurse, or any role that's not 'student'
    if user_role == 'student':
        print(f"⚠️ Mark-read denied for role: {session.get('role')}")
        return jsonify({'error': 'Only staff can mark messages as read'}), 403"""

new_mark = """    # Only staff can mark messages as read (allow all staff roles)
    user_role = session.get('role', '').lower()
    print(f"🔍 Mark-read check: user_role='{user_role}', original role='{session.get('role')}'")
    # Allow: staff, admin, nurse, or any role that's not 'student'
    if user_role == 'student':
        print(f"⚠️ Mark-read denied for role: {session.get('role')}")
        return jsonify({'error': 'Only staff can mark messages as read'}), 403
    print(f"✅ Mark-read allowed for role: {session.get('role')}")"""

content = content.replace(old_mark, new_mark)

# Add debug logging for delete endpoint
old_delete = """    # Only staff can delete consultations (allow all staff roles)
    user_role = session.get('role', '').lower()
    # Allow: staff, admin, nurse, or any role that's not 'student'
    if user_role == 'student':
        print(f"⚠️ Delete denied for role: {session.get('role')}")
        return jsonify({'error': 'Only staff can delete consultations'}), 403"""

new_delete = """    # Only staff can delete consultations (allow all staff roles)
    user_role = session.get('role', '').lower()
    print(f"🔍 Delete check: user_role='{user_role}', original role='{session.get('role')}'")
    # Allow: staff, admin, nurse, or any role that's not 'student'
    if user_role == 'student':
        print(f"⚠️ Delete denied for role: {session.get('role')}")
        return jsonify({'error': 'Only staff can delete consultations'}), 403
    print(f"✅ Delete allowed for role: {session.get('role')}")"""

content = content.replace(old_delete, new_delete)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added debug logging to see actual role values")
print("\nNow restart Flask server and check the console output when you try to delete")

#!/usr/bin/env python3
"""
Fix the consultation chat to display role for ALL user types (Student, Teaching Staff, Non-Teaching Staff, Deans, President)
"""

file_path = r"c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Consultations.html"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Add role field to the data mapping
old_line1 = "                                    patientType: consultation.patientType,"
new_line1 = """                                    patientType: consultation.patientType,
                                    role: consultation.role || consultation.patientType || 'Student', // Add role field for all user types"""

content = content.replace(old_line1, new_line1)

# Fix 2: Update the display to show role instead of patientType
old_line2 = 'x-text="selectedChat.patientType || \'Student\'"'
new_line2 = 'x-text="selectedChat.role || selectedChat.patientType || \'Student\'"'

content = content.replace(old_line2, new_line2)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Successfully updated Staff-Consultations.html")
print("Changes made:")
print("1. Added 'role' field to consultation data mapping")
print("2. Updated chat header to display 'role' for all user types")
print("\nNow the chat will show:")
print("- ROTCHER A. CADORNA JR.")
print("- 2022-0186")
print("- STUDENT (or TEACHING STAFF, NON-TEACHING STAFF, DEANS, PRESIDENT)")

#!/usr/bin/env python3
"""
Remove duplicate role line in Staff-Consultations.html
"""

file_path = r"c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Consultations.html"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and remove duplicate role line
new_lines = []
prev_line = ""
for line in lines:
    # Skip if this line is a duplicate role line
    if "role: consultation.role || consultation.patientType || 'Student', // Add role field for all user types" in line and "role: consultation.role || consultation.patientType || 'Student', // Add role field for all user types" in prev_line:
        continue  # Skip duplicate
    new_lines.append(line)
    prev_line = line

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Successfully removed duplicate role line")

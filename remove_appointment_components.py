import re

# Read the file
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Appointments.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("🔍 Searching for components to remove...")

# 1. Remove the status filter dropdown
status_filter_pattern = r'<select x-model="selectedStatus"[^>]*>.*?</select>'
matches = re.findall(status_filter_pattern, content, re.DOTALL)
if matches:
    print(f"✅ Found status filter dropdown ({len(matches)} occurrence(s))")
    content = re.sub(status_filter_pattern, '', content, flags=re.DOTALL)

# 2. Remove the export button
export_button_pattern = r'<button @click="exportAppointments\(\)"[^>]*>.*?</button>'
matches = re.findall(export_button_pattern, content, re.DOTALL)
if matches:
    print(f"✅ Found export button ({len(matches)} occurrence(s))")
    content = re.sub(export_button_pattern, '', content, flags=re.DOTALL)

# 3. Remove the green pulse dot
pulse_dot_pattern = r'<div class="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>'
matches = re.findall(pulse_dot_pattern, content, re.DOTALL)
if matches:
    print(f"✅ Found green pulse dot ({len(matches)} occurrence(s))")
    content = re.sub(pulse_dot_pattern, '', content, flags=re.DOTALL)

# Write back
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Appointments.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ All specified components removed successfully!")
print("📝 Components removed:")
print("   - Status filter dropdown (All Status, Pending, Confirmed, etc.)")
print("   - Export button")
print("   - Green pulse animation dot")

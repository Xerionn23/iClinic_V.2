import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html'

print("🔧 Fixing nurse role to stay as 'Clinic Nurse' instead of changing to admin...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace the loadAssignedStaff function to filter only nurses
    old_code = '''            if (response.ok) {
                const staffList = await response.json();
                if (staffList && staffList.length > 0) {
                    // Get the first available staff member (in a real system, this would be assigned)
                    const staff = staffList[0];
                    staffName = `${staff.first_name} ${staff.last_name}`;
                    staffPosition = staff.position || 'Registered Nurse';
                }
            }'''
    
    new_code = '''            if (response.ok) {
                const staffList = await response.json();
                if (staffList && staffList.length > 0) {
                    // Filter to get only nurses (not admins or other staff)
                    const nurses = staffList.filter(staff => 
                        staff.position && (
                            staff.position.toLowerCase().includes('nurse') ||
                            staff.role === 'nurse'
                        )
                    );
                    
                    if (nurses.length > 0) {
                        // Get the first available nurse
                        const staff = nurses[0];
                        staffName = `${staff.first_name} ${staff.last_name}`;
                        staffPosition = staff.position || 'Registered Nurse';
                    }
                    // If no nurses found, keep default "Clinic Nurse"
                }
            }'''
    
    content = content.replace(old_code, new_code)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully fixed nurse role filtering!\n")
        print("📋 Changes made:")
        print("   ✅ Added filter to get only nurses from staff list")
        print("   ✅ Excludes System Administrator and other non-nurse roles")
        print("   ✅ Keeps 'Clinic Nurse' as default if no nurses found")
        print("\n✨ Result:")
        print("   - Will show 'Clinic Nurse' consistently")
        print("   - Won't change to 'System Administrator'")
        print("   - Only displays actual nurses from the system")
    else:
        print("⚠️  Pattern not found or already fixed")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

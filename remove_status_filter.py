import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html'

print("🔧 Removing status filter dropdown from appointments...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to match the entire select dropdown with all its options
    pattern = r'<select x-model="selectedStatus"[^>]*>[\s\S]*?<option value="">All Status</option>[\s\S]*?<option value="Pending">Pending</option>[\s\S]*?<option value="Confirmed">Confirmed</option>[\s\S]*?<option value="Completed">Completed</option>[\s\S]*?<option value="Cancelled">Cancelled</option>[\s\S]*?</select>\s*'
    
    content = re.sub(pattern, '', content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully removed status filter dropdown!")
        print("\n📋 What was removed:")
        print("   - Status filter dropdown (All Status, Pending, Confirmed, etc.)")
        print("   - Only 'Request Appointment' button remains")
    else:
        print("⚠️  Pattern not found or already removed")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

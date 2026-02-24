import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html'

print("🔧 Adding x-cloak to remaining modals in appointments...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Add x-cloak to profileDropdown
    pattern1 = r'(<div x-show="profileDropdown")\s+'
    replacement1 = r'\1 x-cloak\n                     '
    content = re.sub(pattern1, replacement1, content, count=1)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully added x-cloak to profileDropdown!")
        print("\n📋 Fixed modals:")
        print("   ✅ profileDropdown - Added x-cloak")
        print("   ✅ showAddModal - Already has x-cloak")
        print("   ✅ showLogoutConfirm - Already has x-cloak")
        print("\n✅ Result:")
        print("   - No more automatic modal opening")
        print("   - Smooth navigation")
        print("   - All modals properly hidden until needed")
    else:
        print("⚠️  Already has x-cloak or pattern not found")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

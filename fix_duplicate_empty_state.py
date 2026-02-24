import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-health-records.html'

print("🔧 Fixing duplicate empty state in ST-health-records.html...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to match the duplicate empty state (the second one around line 856-860)
    # This is the one that appears AFTER the mobile cards section
    pattern = r'\s*<!-- Empty State \(if needed\) -->\s*<div x-show="medicalRecords\.length === 0" class="text-center py-8">\s*<span class="text-4xl">📋</span>\s*<p class="mt-2 text-gray-500">No clinic visits recorded yet</p>\s*</div>\s*'
    
    content = re.sub(pattern, '\n                        ', content, flags=re.DOTALL)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully removed duplicate empty state!")
        print("\n📋 What was removed:")
        print("   - Duplicate 'No clinic visits recorded yet' message")
        print("   - Line ~857-860")
        print("\n✅ What remains:")
        print("   - Single 'No Medical Records Found' message (line ~729-733)")
        print("   - Shows when loading is complete and no records exist")
    else:
        print("⚠️  Pattern not found or already fixed")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

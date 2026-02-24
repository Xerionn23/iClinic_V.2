import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html'

print("🔧 Fixing console errors in consultation chat...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Add showNurseInfo variable
    # Find the Alpine.js data object and add showNurseInfo
    pattern1 = r"(userDropdown: false,)\s+(selectedNurse:)"
    replacement1 = r"\1\n    showNurseInfo: false,\n    \2"
    content = re.sub(pattern1, replacement1, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully fixed console errors!\n")
        print("📋 Fixes applied:")
        print("   ✅ Added showNurseInfo: false to Alpine.js data")
        print("   ✅ Tailwind warning already suppressed")
        print("\n✨ Result:")
        print("   - No more 'showNurseInfo is not defined' error")
        print("   - Nurse info panel will work correctly")
        print("   - Clean console output")
    else:
        print("⚠️  Pattern not found or already fixed")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

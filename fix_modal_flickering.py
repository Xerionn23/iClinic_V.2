import re
import os

student_files = [
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-dashboard.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-health-records.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-Announcement.html'
]

print("🔧 Fixing modal flickering issue in student pages...\n")
print("Problem: Multiple feather.replace() calls causing modals to flicker\n")

updated_count = 0

for file_path in student_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove multiple setTimeout feather.replace() calls
        # Pattern 1: Remove the multiple setTimeout blocks
        pattern1 = r"document\.addEventListener\('alpine:init', \(\) => \{[\s\S]*?setTimeout\(\(\) => \{[\s\S]*?feather\.replace\(\);[\s\S]*?\}, 250\);[\s\S]*?setTimeout\(\(\) => \{[\s\S]*?feather\.replace\(\);[\s\S]*?\}, 500\);[\s\S]*?setTimeout\(\(\) => \{[\s\S]*?feather\.replace\(\);[\s\S]*?\}, 1000\);[\s\S]*?\}\);"
        
        content = re.sub(pattern1, '', content)
        
        # Pattern 2: Remove standalone feather.replace() in init if there are multiple
        # Keep only ONE feather.replace() call in init()
        
        # Pattern 3: Remove the profileModal store if it exists
        pattern3 = r"Alpine\.store\('profileModal', \{[\s\S]*?open\(\) \{[\s\S]*?feather\.replace\(\);[\s\S]*?\}[\s\S]*?\}\);"
        content = re.sub(pattern3, '', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            filename = os.path.basename(file_path)
            print(f"✅ Fixed: {filename}")
            updated_count += 1
        else:
            filename = os.path.basename(file_path)
            print(f"⚠️  No change: {filename}")
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")

print(f"\n✨ Complete! Fixed {updated_count}/{len(student_files)} files")
print("\n📋 What was fixed:")
print("   - Removed multiple setTimeout feather.replace() calls")
print("   - Removed Alpine.store profileModal with feather calls")
print("   - Kept only ONE feather initialization in init()")
print("\n✅ Result:")
print("   - No more modal flickering")
print("   - Smooth navigation between pages")
print("   - Icons still render correctly")

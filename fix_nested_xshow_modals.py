import re
import os

student_files = [
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-dashboard.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-health-records.html',
]

print("🔧 Fixing nested x-show in modals causing flickering...\n")
print("Problem: Duplicate x-show directives on parent and child divs\n")

updated_count = 0

for file_path in student_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix Pattern 1: Profile Modal - remove inner x-show
        pattern1 = r'(<div x-show="profileModal"[^>]*>)\s*<div x-show="profileModal"'
        replacement1 = r'\1\n        <div'
        content = re.sub(pattern1, replacement1, content)
        
        # Fix Pattern 2: Settings Modal - remove inner x-show
        pattern2 = r'(<div x-show="settingsModal"[^>]*>)\s*<div x-show="settingsModal"'
        replacement2 = r'\1\n        <div'
        content = re.sub(pattern2, replacement2, content)
        
        # Fix Pattern 3: All Notifications Modal - remove inner x-show
        pattern3 = r'(<div x-show="allNotificationsModal"[^>]*>)\s*<div x-show="allNotificationsModal"'
        replacement3 = r'\1\n        <div'
        content = re.sub(pattern3, replacement3, content)
        
        # Fix Pattern 4: Any other modal with nested x-show
        pattern4 = r'(<div x-show="showModal"[^>]*>)\s*<div x-show="showModal"'
        replacement4 = r'\1\n        <div'
        content = re.sub(pattern4, replacement4, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            filename = os.path.basename(file_path)
            print(f"✅ Fixed: {filename}")
            updated_count += 1
        else:
            filename = os.path.basename(file_path)
            print(f"⚠️  No nested x-show found: {filename}")
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")

print(f"\n✨ Complete! Fixed {updated_count}/{len(student_files)} files")
print("\n📋 What was fixed:")
print("   - Removed duplicate x-show on inner modal divs")
print("   - Kept only ONE x-show on outer modal container")
print("   - Prevents double animation/flickering")
print("\n✅ Result:")
print("   - No more modal flickering")
print("   - Smooth modal transitions")
print("   - Proper show/hide behavior")

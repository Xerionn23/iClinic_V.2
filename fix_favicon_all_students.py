import re
import os

student_files = [
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-dashboard.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-health-records.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-Announcement.html'
]

print("🔧 Fixing favicon to use NC logo for all student pages...\n")

# Old SVG favicon pattern
old_favicon_pattern = r'<link rel="icon" type="image/svg\+xml" href="data:image/svg\+xml[^"]*">\s*<link rel="apple-touch-icon" href="data:image/svg\+xml[^"]*">'

# New NC logo favicon
new_favicon = '''<link rel="icon" type="image/png" href="../assets/img/iclinic-logo.png">
    <link rel="apple-touch-icon" href="../assets/img/iclinic-logo.png">'''

updated_count = 0

for file_path in student_files:
    try:
        filename = os.path.basename(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace old SVG favicon with NC logo
        content = re.sub(old_favicon_pattern, new_favicon, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename} - Updated favicon to NC logo")
            updated_count += 1
        else:
            print(f"⚠️  {filename} - No change (already correct or pattern not found)")
            
    except Exception as e:
        print(f"❌ Error processing {filename}: {str(e)}")

print(f"\n✨ Complete! Updated {updated_count}/{len(student_files)} files")
print("\n📋 What was changed:")
print("   - Removed SVG heartbeat icon")
print("   - Added NC logo (iclinic-logo.png)")
print("   - Applied to both favicon and apple-touch-icon")
print("\n✅ Result:")
print("   - Browser tab now shows NC logo")
print("   - Professional branding across all pages")
print("   - Consistent with sidebar logo")

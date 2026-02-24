import re

files_to_fix = [
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-health-records.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-Announcement.html'
]

favicon_html = '''    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="../assets/img/iclinic-logo.png">
    <link rel="apple-touch-icon" href="../assets/img/iclinic-logo.png">
'''

print("🔧 Adding NC logo favicon to remaining files...\n")

for file_path in files_to_fix:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add favicon after <title> tag
        content = re.sub(
            r'(</title>)',
            r'\1' + favicon_html,
            content,
            count=1
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        filename = file_path.split('\\')[-1]
        print(f"✅ {filename} - Added NC logo favicon")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n✨ Complete! All student pages now have NC logo favicon!")

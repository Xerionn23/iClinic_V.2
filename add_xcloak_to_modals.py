import re
import os

student_files = [
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-dashboard.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-health-records.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-Announcement.html'
]

print("🔧 Adding x-cloak to modals to prevent flickering...\n")

# x-cloak CSS to add
xcloak_css = '''        
        /* Prevent modal flash before Alpine loads */
        [x-cloak] { display: none !important; }
'''

updated_count = 0

for file_path in student_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Step 1: Add x-cloak CSS if not exists
        if '[x-cloak]' not in content:
            # Find </style> tag and add before it
            content = content.replace('</style>', xcloak_css + '    </style>')
        
        # Step 2: Add x-cloak to modal divs
        # Pattern for modals with x-show
        modals_to_fix = [
            'profileModal',
            'settingsModal',
            'allNotificationsModal',
            'showModal',
            'showAddModal'
        ]
        
        for modal_name in modals_to_fix:
            # Add x-cloak to modal divs that don't have it
            pattern = f'(<div x-show="{modal_name}"(?![^>]*x-cloak))'
            replacement = f'\\1 x-cloak'
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            filename = os.path.basename(file_path)
            print(f"✅ Fixed: {filename}")
            updated_count += 1
        else:
            filename = os.path.basename(file_path)
            print(f"⚠️  No changes: {filename}")
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")

print(f"\n✨ Complete! Fixed {updated_count}/{len(student_files)} files")
print("\n📋 What was added:")
print("   - [x-cloak] CSS rule to hide elements before Alpine loads")
print("   - x-cloak attribute to all modal divs")
print("\n✅ Result:")
print("   - Modals won't flash/flicker on page load")
print("   - Smooth modal appearance")
print("   - No FOUC (Flash of Unstyled Content)")

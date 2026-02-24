import re

# All student pages
student_files = [
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-dashboard.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-health-records.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-Announcement.html'
]

print("🔧 Adding chevron arrow to student profile dropdown...\n")

chevron_icon = '''                        <!-- Chevron Icon -->
                        <svg x-show="!sidebarCollapsed || sidebarHovered" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 text-white/70 flex-shrink-0">
                            <polyline points="18 15 12 9 6 15"></polyline>
                        </svg>
'''

updated_count = 0

for file_path in student_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to find the profile button and add chevron before closing button tag
        # Look for the user info div, then add chevron before </button>
        pattern = r'(<div x-show="!sidebarCollapsed \|\| sidebarHovered" x-transition class="text-left">.*?</div>)\s*(</button>)'
        
        replacement = r'\1\n' + chevron_icon + r'                    \2'
        
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            filename = file_path.split('\\')[-1]
            print(f"✅ Updated: {filename}")
            updated_count += 1
        else:
            filename = file_path.split('\\')[-1]
            print(f"⚠️  No change: {filename} (already has chevron or pattern not found)")
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")

print(f"\n✨ Complete! Updated {updated_count}/{len(student_files)} files")
print("\n📋 What was added:")
print("   - Chevron up arrow icon (▲)")
print("   - Shows next to user name in profile button")
print("   - Indicates dropdown functionality")
print("   - Matches Nurse UI design")

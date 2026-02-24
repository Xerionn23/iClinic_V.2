import os
import re

# List of files to update
student_files = [
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-Announcement.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-dashboard.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-health-records.html'
]

def fix_navigation(file_path):
    """Remove Profile and Settings buttons from navigation dropdown, keep only Logout"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match the Profile and Settings buttons plus the hr separator
        # We want to remove everything between the dropdown opening and the logout link
        pattern = r'(<button[^>]*@click="profileModal[^>]*>.*?</button>\s*<button[^>]*@click="settingsModal[^>]*>.*?</button>\s*<hr[^>]*>\s*)'
        
        # Replace with just whitespace to maintain structure
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Alternative pattern if the first one doesn't match
        if content == original_content:
            # Try matching just the buttons without modal references
            pattern2 = r'(<button[^>]*class="w-full flex items-center gap-3[^>]*>\s*<i data-feather="user"[^>]*></i>\s*<span>Profile</span>\s*</button>\s*<button[^>]*class="w-full flex items-center gap-3[^>]*>\s*<i data-feather="settings"[^>]*></i>\s*<span>Settings</span>\s*</button>\s*<hr[^>]*>\s*)'
            content = re.sub(pattern2, '', content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {os.path.basename(file_path)}")
            return True
        else:
            print(f"⚠️  No changes needed or pattern not found: {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def main():
    print("🔧 Fixing navigation dropdowns across all student dashboards...\n")
    
    success_count = 0
    for file_path in student_files:
        if fix_navigation(file_path):
            success_count += 1
    
    print(f"\n✨ Complete! Updated {success_count}/{len(student_files)} files")
    print("\n📋 Changes made:")
    print("   - Removed 'Profile' button from dropdown")
    print("   - Removed 'Settings' button from dropdown")
    print("   - Kept only 'Logout' button")

if __name__ == "__main__":
    main()

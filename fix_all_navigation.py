import os
import re

# All files to update
files_to_update = [
    # Staff pages
    r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Announcement.html',
    r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Appointments.html',
    r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Consultations.html',
    r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Dashboard.html',
    r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Inventory.html',
    r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Patients.html',
    r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html',
    # Deans/President pages
    r'c:\xampp\htdocs\iClini V.2\pages\deans_president\DEANS_REPORT.html',
    r'c:\xampp\htdocs\iClini V.2\pages\deans_president\Deans_consultationchat.html',
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
        
        # Pattern 1: Match Profile and Settings buttons with modal references
        pattern1 = r'(<button[^>]*@click="profileModal[^>]*>.*?</button>\s*<button[^>]*@click="settingsModal[^>]*>.*?</button>\s*<hr[^>]*>\s*)'
        content = re.sub(pattern1, '', content, flags=re.DOTALL)
        
        # Pattern 2: Match Profile and Settings buttons without modal references (just links/buttons)
        if content == original_content:
            pattern2 = r'(<button[^>]*class="w-full flex items-center gap-3[^>]*>\s*<i data-feather="user"[^>]*></i>\s*<span>Profile</span>\s*</button>\s*<button[^>]*class="w-full flex items-center gap-3[^>]*>\s*<i data-feather="settings"[^>]*></i>\s*<span>Settings</span>\s*</button>\s*<hr[^>]*>\s*)'
            content = re.sub(pattern2, '', content, flags=re.DOTALL)
        
        # Pattern 3: Match <a> tags for Profile and Settings
        if content == original_content:
            pattern3 = r'(<a[^>]*>\s*<i data-feather="user"[^>]*></i>\s*<span>Profile</span>\s*</a>\s*<a[^>]*>\s*<i data-feather="settings"[^>]*></i>\s*<span>Settings</span>\s*</a>\s*<hr[^>]*>\s*)'
            content = re.sub(pattern3, '', content, flags=re.DOTALL)
        
        # Pattern 4: More flexible pattern for any Profile/Settings combination
        if content == original_content:
            # Remove Profile button/link
            pattern4a = r'<(?:button|a)[^>]*>\s*<i data-feather="user"[^>]*></i>\s*<span>Profile</span>\s*</(?:button|a)>\s*'
            content = re.sub(pattern4a, '', content, flags=re.DOTALL)
            
            # Remove Settings button/link
            pattern4b = r'<(?:button|a)[^>]*>\s*<i data-feather="settings"[^>]*></i>\s*<span>Settings</span>\s*</(?:button|a)>\s*'
            content = re.sub(pattern4b, '', content, flags=re.DOTALL)
            
            # Remove hr separator if it exists before logout
            pattern4c = r'<hr[^>]*>\s*(?=<(?:a|button)[^>]*(?:logout|log-out))'
            content = re.sub(pattern4c, '', content, flags=re.DOTALL | re.IGNORECASE)
        
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
    print("🔧 Fixing navigation dropdowns across ALL pages...\n")
    print("📁 Updating:")
    print("   - Staff pages (7 files)")
    print("   - Deans/President pages (2 files)")
    print()
    
    success_count = 0
    for file_path in files_to_update:
        if fix_navigation(file_path):
            success_count += 1
    
    print(f"\n✨ Complete! Updated {success_count}/{len(files_to_update)} files")
    print("\n📋 Changes made:")
    print("   - Removed 'Profile' button from dropdown")
    print("   - Removed 'Settings' button from dropdown")
    print("   - Removed separator line (hr)")
    print("   - Kept only 'Logout' button")
    print("\n✅ Navigation simplified across:")
    print("   ✓ All Student pages")
    print("   ✓ All Staff pages")
    print("   ✓ All Deans/President pages")

if __name__ == "__main__":
    main()

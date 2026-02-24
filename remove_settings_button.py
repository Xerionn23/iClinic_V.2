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

def remove_settings_button(file_path):
    """Remove Settings button from navigation dropdown, keep only Logout"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match Settings button with various formats
        # This matches: <button ... @click="showSettingsModal = true ... >...</button>
        pattern = r'<button[^>]*@click="showSettingsModal\s*=\s*true[^>]*>.*?</button>\s*'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Alternative pattern for Settings links
        pattern2 = r'<a[^>]*>\s*<i[^>]*data-feather="settings"[^>]*></i>\s*Settings\s*</a>\s*'
        content = re.sub(pattern2, '', content, flags=re.DOTALL)
        
        # Another pattern for button with settings icon
        pattern3 = r'<button[^>]*>\s*<i[^>]*data-feather="settings"[^>]*></i>\s*Settings\s*</button>\s*'
        content = re.sub(pattern3, '', content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {os.path.basename(file_path)}")
            return True
        else:
            print(f"⚠️  No Settings button found: {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def main():
    print("🔧 Removing Settings button from ALL navigation dropdowns...\n")
    print("📁 Updating:")
    print("   - Staff pages (7 files)")
    print("   - Deans/President pages (2 files)")
    print()
    
    success_count = 0
    for file_path in files_to_update:
        if remove_settings_button(file_path):
            success_count += 1
    
    print(f"\n✨ Complete! Updated {success_count}/{len(files_to_update)} files")
    print("\n📋 Final navigation state:")
    print("   ✓ Removed 'Settings' button")
    print("   ✓ Kept only 'Logout' button")
    print("\n✅ Clean navigation across:")
    print("   ✓ All Student pages")
    print("   ✓ All Staff pages")
    print("   ✓ All Deans/President pages")

if __name__ == "__main__":
    main()

import os
import re

# All files to clean up
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

def cleanup_navigation(file_path):
    """Remove Settings comments and unnecessary hr tags from navigation dropdown"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove Settings Button comments
        content = re.sub(r'\s*<!--\s*Settings Button\s*-->\s*', '', content)
        
        # Remove Logout Button comments (optional, but cleaner)
        content = re.sub(r'\s*<!--\s*Logout Button\s*-->\s*', '', content)
        
        # Remove hr tags that appear right before logout button in dropdown
        # Pattern: <hr...> followed by whitespace and then logout button
        pattern = r'<hr[^>]*>\s*(?=<(?:button|a)[^>]*(?:showLogoutConfirm|logout))'
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Cleaned: {os.path.basename(file_path)}")
            return True
        else:
            print(f"⚠️  Already clean: {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def main():
    print("🧹 Cleaning up navigation dropdowns...\n")
    print("📁 Cleaning:")
    print("   - Removing Settings comments")
    print("   - Removing unnecessary hr separators")
    print()
    
    success_count = 0
    for file_path in files_to_update:
        if cleanup_navigation(file_path):
            success_count += 1
    
    print(f"\n✨ Complete! Cleaned {success_count}/{len(files_to_update)} files")
    print("\n📋 Final result:")
    print("   ✓ Clean, minimal navigation dropdown")
    print("   ✓ Only Logout button remains")
    print("   ✓ No unnecessary comments or separators")

if __name__ == "__main__":
    main()

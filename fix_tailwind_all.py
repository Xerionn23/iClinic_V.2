import os
import re

# List of all HTML files to fix
html_files = [
    r"STUDENT\ST-Announcement.html",
    r"STUDENT\ST-appointment.html",
    r"STUDENT\ST-consulatation-chat.html",
    r"STUDENT\ST-dashboard.html",
    r"STUDENT\ST-health-records.html",
    r"pages\admin\ADMIN-dashboard.html",
    r"pages\admin\PRINT-REPORTS.html",
    r"pages\admin\REPORTS.html",
    r"pages\deans_president\DEANS_REPORT.html",
    r"pages\deans_president\Deans_consultationchat.html",
    r"pages\public\404.html",
    r"pages\public\500.html",
    r"pages\public\complete-registration.html",
    r"pages\public\online-consultation.html",
    r"pages\public\verification-result.html",
    r"pages\staff\Staff-Announcement.html",
    r"pages\staff\Staff-Appointments.html",
    r"pages\staff\Staff-Consultations.html",
    r"pages\staff\Staff-Dashboard.html",
    r"pages\staff\Staff-Inventory.html",
    r"pages\staff\Staff-Patients.html",
    r"pages\staff\Staff-Reports.html",
]

base_dir = r"c:\xampp\htdocs\iClini V.2"

def fix_tailwind_in_file(filepath):
    """Fix Tailwind CSS loading in HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file uses tailwind.min.css
        if 'tailwind.min.css' not in content:
            print(f"⏭️  Skipped (no tailwind.min.css): {filepath}")
            return False
        
        # Pattern 1: Remove warning suppression script + link + config
        pattern1 = r'<script>\s*(?://[^\n]*\n\s*)?(?:const originalWarn|console\.warn|\(function\(\)|var originalWarn).*?</script>\s*<link rel="stylesheet" href="/assets/css/libs/tailwind\.min\.css">\s*(?:<script>\s*tailwind\.config\s*=\s*\{.*?</script>)?'
        
        # Pattern 2: Just link without scripts
        pattern2 = r'<link rel="stylesheet" href="/assets/css/libs/tailwind\.min\.css">'
        
        # Replacement: Simple CDN script
        replacement = '<script src="https://cdn.tailwindcss.com"></script>'
        
        # Try pattern 1 first (with scripts)
        new_content = re.sub(pattern1, replacement, content, flags=re.DOTALL)
        
        # If no change, try pattern 2 (just link)
        if new_content == content:
            new_content = re.sub(pattern2, replacement, content)
        
        # Check if anything changed
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Fixed: {filepath}")
            return True
        else:
            print(f"⚠️  No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {filepath}: {str(e)}")
        return False

def main():
    print("🔧 Fixing Tailwind CSS in all HTML files...\n")
    
    fixed_count = 0
    total_count = len(html_files)
    
    for html_file in html_files:
        filepath = os.path.join(base_dir, html_file)
        if os.path.exists(filepath):
            if fix_tailwind_in_file(filepath):
                fixed_count += 1
        else:
            print(f"❌ File not found: {filepath}")
    
    print(f"\n{'='*60}")
    print(f"✨ Fixed {fixed_count} out of {total_count} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

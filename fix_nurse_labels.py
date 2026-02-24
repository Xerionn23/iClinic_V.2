import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html'

print("🔧 Updating consultation chat to show 'Nurse' instead of 'Healthcare Staff'...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace all healthcare staff references with Nurse
    replacements = [
        ('Healthcare Staff', 'Clinic Nurse'),
        ('Healthcare Specialist', 'Registered Nurse'),
        ('Senior Healthcare Specialist', 'Registered Nurse'),
        ("name: 'Nurse Maria Santos'", "name: 'Clinic Nurse'"),
        ("avatar: 'MS'", "avatar: 'CN'"),
        ("let staffName = 'Healthcare Staff'", "let staffName = 'Clinic Nurse'"),
        ("let staffPosition = 'Healthcare Specialist'", "let staffPosition = 'Registered Nurse'"),
    ]
    
    changes_made = []
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            changes_made.append(f"   ✅ {old} → {new}")
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully updated nurse labels!\n")
        print("📋 Changes made:")
        for change in changes_made:
            print(change)
        print("\n✨ Result:")
        print("   - Chat shows 'Clinic Nurse' as the healthcare provider")
        print("   - Avatar shows 'CN' (Clinic Nurse)")
        print("   - Specialty shows 'Registered Nurse'")
        print("   - Professional and clear labeling")
    else:
        print("⚠️  No changes needed or already updated")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

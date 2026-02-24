import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html'

print("🔧 Fixing card icons in appointments page...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Add additional feather.replace() call after longer delay
    # Find the section after loadClinicEvents() and add another refresh
    pattern = r"(await this\.loadClinicEvents\(\);)\s+(// Refresh feather icons after data loads)"
    
    replacement = r'''\1
                    
                    // Ensure icons render in cards
                    this.$nextTick(() => {
                        setTimeout(() => {
                            if (typeof feather !== 'undefined') {
                                feather.replace();
                                console.log('✅ Card icons refreshed');
                            }
                        }, 100);
                    });
                    
                    \2'''
    
    content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully added icon refresh for cards!")
        print("\n📋 What was added:")
        print("   - Additional feather.replace() in $nextTick")
        print("   - Runs after data loads")
        print("   - Ensures card icons render properly")
        print("\n✅ Result:")
        print("   - Icons in cards will display correctly")
        print("   - Calendar, clock, and other icons visible")
    else:
        print("⚠️  Pattern not found - trying alternative fix...")
        
        # Alternative: Just add a final feather.replace() at the end of init
        pattern2 = r"(console\.log\('✅ Feather icons refreshed after data load'\);)"
        replacement2 = r'''\1
                        
                        // Additional refresh for cards
                        setTimeout(() => {
                            if (typeof feather !== 'undefined') {
                                feather.replace();
                                console.log('✅ Card icons final refresh');
                            }
                        }, 1000);'''
        
        content = original_content
        content = re.sub(pattern2, replacement2, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Applied alternative fix - added delayed icon refresh")
        else:
            print("❌ Could not apply fix")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

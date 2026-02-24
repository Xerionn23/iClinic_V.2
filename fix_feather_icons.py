import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html'

print("🔧 Fixing Feather icons initialization in ST-appointment.html...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace all feather.replace() calls with safe version
    safe_feather_code = '''// Safe feather icon initialization
                    setTimeout(() => {
                        if (typeof feather !== 'undefined') {
                            try {
                                // Get all elements with data-feather attribute
                                const icons = document.querySelectorAll('[data-feather]');
                                icons.forEach(icon => {
                                    const iconName = icon.getAttribute('data-feather');
                                    // Check if icon exists in feather library
                                    if (feather.icons[iconName]) {
                                        // Icon is valid, safe to replace
                                    } else {
                                        console.warn(`⚠️ Invalid feather icon: ${iconName}`);
                                        // Remove invalid icon attribute to prevent errors
                                        icon.removeAttribute('data-feather');
                                    }
                                });
                                // Now safely replace all valid icons
                                feather.replace();
                            } catch (error) {
                                console.error('❌ Feather icons error:', error);
                            }
                        }
                    }, 100);'''
    
    # Pattern 1: First feather.replace() call (around line 1320)
    pattern1 = r'// Initialize feather icons\s+setTimeout\(\(\) => \{\s+if \(typeof feather !== \'undefined\'\) \{\s+feather\.replace\(\);\s+\}\s+\}, 100\);'
    content = re.sub(pattern1, safe_feather_code, content, flags=re.DOTALL)
    
    # Pattern 2: Second feather.replace() call (around line 1347)
    pattern2 = r'// Refresh feather icons after data loads\s+setTimeout\(\(\) => \{\s+if \(typeof feather !== \'undefined\'\) \{\s+feather\.replace\(\);\s+console\.log\(\'✅ Feather icons refreshed after data load\'\);\s+\}\s+\}, 500\);'
    safe_feather_code2 = '''// Refresh feather icons after data loads
                    setTimeout(() => {
                        if (typeof feather !== 'undefined') {
                            try {
                                const icons = document.querySelectorAll('[data-feather]');
                                icons.forEach(icon => {
                                    const iconName = icon.getAttribute('data-feather');
                                    if (!feather.icons[iconName]) {
                                        console.warn(`⚠️ Invalid feather icon: ${iconName}`);
                                        icon.removeAttribute('data-feather');
                                    }
                                });
                                feather.replace();
                                console.log('✅ Feather icons refreshed after data load');
                            } catch (error) {
                                console.error('❌ Feather icons error:', error);
                            }
                        }
                    }, 500);'''
    content = re.sub(pattern2, safe_feather_code2, content, flags=re.DOTALL)
    
    # Pattern 3: Third feather.replace() call (around line 1716)
    pattern3 = r'// Refresh feather icons\s+setTimeout\(\(\) => \{\s+if \(typeof feather !== \'undefined\'\) \{\s+feather\.replace\(\);\s+\}\s+\}, 100\);'
    safe_feather_code3 = '''// Refresh feather icons
                            setTimeout(() => {
                                if (typeof feather !== 'undefined') {
                                    try {
                                        const icons = document.querySelectorAll('[data-feather]');
                                        icons.forEach(icon => {
                                            const iconName = icon.getAttribute('data-feather');
                                            if (!feather.icons[iconName]) {
                                                icon.removeAttribute('data-feather');
                                            }
                                        });
                                        feather.replace();
                                    } catch (error) {
                                        console.error('❌ Feather icons error:', error);
                                    }
                                }
                            }, 100);'''
    content = re.sub(pattern3, safe_feather_code3, content, flags=re.DOTALL)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully fixed Feather icons initialization!")
        print("\n📋 Changes made:")
        print("   - Added validation for icon names before replace()")
        print("   - Added try-catch error handling")
        print("   - Invalid icons are removed to prevent errors")
        print("   - Console warnings for debugging")
    else:
        print("⚠️  Pattern not found - using alternative fix method...")
        
        # Alternative: Just wrap all feather.replace() with try-catch
        content = re.sub(
            r'feather\.replace\(\);',
            '''try { feather.replace(); } catch(e) { console.error('Feather error:', e); }''',
            original_content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Applied alternative fix - wrapped feather.replace() with try-catch")
        else:
            print("❌ Could not apply fix")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

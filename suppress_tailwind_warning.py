import os
import re

# Find all HTML files that use Tailwind CDN
html_files = []

# Search in all directories
for root, dirs, files in os.walk(r'c:\xampp\htdocs\iClini V.2'):
    # Skip node_modules and .venv
    if 'node_modules' in root or '.venv' in root or '__pycache__' in root:
        continue
    
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            html_files.append(file_path)

print(f"🔍 Found {len(html_files)} HTML files\n")

# Add script to suppress Tailwind warning
suppress_script = '''    <!-- Suppress Tailwind CDN Warning -->
    <script>
        // Suppress Tailwind CDN production warning
        const originalWarn = console.warn;
        console.warn = function(...args) {
            if (args[0] && typeof args[0] === 'string' && args[0].includes('cdn.tailwindcss.com')) {
                return; // Suppress Tailwind CDN warning
            }
            originalWarn.apply(console, args);
        };
    </script>
'''

updated_count = 0

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file uses Tailwind CDN
        if 'cdn.tailwindcss.com' not in content:
            continue
        
        # Check if warning suppression already exists
        if 'Suppress Tailwind CDN Warning' in content:
            continue
        
        original_content = content
        
        # Add suppression script after Tailwind CDN script
        pattern = r'(<script src="https://cdn\.tailwindcss\.com"></script>)'
        replacement = r'\1' + suppress_script
        
        content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {os.path.basename(file_path)}")
            updated_count += 1
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")

print(f"\n✨ Complete! Updated {updated_count} files")
print("\n📋 What was done:")
print("   - Added console.warn suppression script")
print("   - Filters out Tailwind CDN warnings")
print("   - Other warnings still show normally")
print("\n✅ The Tailwind CDN warning will no longer appear in console!")

import datetime

# Read the file
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add cache-busting comment at the top
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cache_buster = f'<!-- CACHE BUSTER: {timestamp} -->\n'

# Check if there's already a cache buster and replace it
if '<!-- CACHE BUSTER:' in content:
    import re
    content = re.sub(r'<!-- CACHE BUSTER: .+ -->\n', cache_buster, content)
else:
    # Add at the very beginning
    content = cache_buster + content

# Write back
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Cache buster added: {timestamp}")
print("🔄 Please do a HARD REFRESH in your browser:")
print("   - Windows: Ctrl + Shift + R or Ctrl + F5")
print("   - Mac: Cmd + Shift + R")

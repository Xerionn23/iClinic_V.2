import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html'

print("🔧 Moving Alpine.js data from inline x-data to Alpine.data() component...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Change x-data from inline object to component reference
    # Find: <body class="..." x-data="{
    # Replace with: <body class="..." x-data="consultationChat()">
    
    pattern = r'(<body[^>]*) x-data="\{[^}]*$'
    
    # First, let's just change the opening
    content = re.sub(
        r'(<body[^>]*class="[^"]*")\s+x-data="\{',
        r'\1 x-data="consultationChat()">\n<script>\nfunction consultationChat() {\n    return {',
        content,
        count=1
    )
    
    # Then change the closing
    content = re.sub(
        r'\}" x-init="init\(\)">',
        r'    };\n}\n</script>',
        content,
        count=1
    )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully moved Alpine data to component!")
        print("\n📋 Changes:")
        print("   - Changed x-data from inline object to function call")
        print("   - Wrapped data in consultationChat() function")
        print("   - Moved to <script> tag for better parsing")
        print("\n✅ This should fix all the syntax errors!")
    else:
        print("⚠️  No changes made")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

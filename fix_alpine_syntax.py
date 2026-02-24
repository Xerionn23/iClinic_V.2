import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html'

print("🔧 Fixing Alpine.js syntax errors in consultation chat...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the x-data block
    start_marker = 'x-data="{'
    end_marker = '}" x-init="init()">'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("❌ Could not find x-data block")
    else:
        xdata_block = content[start_idx:end_idx + len(end_marker)]
        print(f"✅ Found x-data block: {len(xdata_block)} characters")
        print(f"   Start: position {start_idx}")
        print(f"   End: position {end_idx}")
        
        # Count braces to check balance
        open_braces = xdata_block.count('{')
        close_braces = xdata_block.count('}')
        open_parens = xdata_block.count('(')
        close_parens = xdata_block.count(')')
        
        print(f"\n📊 Brace/Paren Count:")
        print(f"   {{ : {open_braces}")
        print(f"   }} : {close_braces}")
        print(f"   ( : {open_parens}")
        print(f"   ) : {close_parens}")
        
        if open_braces != close_braces:
            print(f"\n⚠️  UNBALANCED BRACES: {open_braces - close_braces} difference")
        if open_parens != close_parens:
            print(f"⚠️  UNBALANCED PARENTHESES: {open_parens - close_parens} difference")
        
        # The issue is likely the x-data ends with }" but should just be }
        # Let's check the exact ending
        ending_section = content[end_idx-50:end_idx+50]
        print(f"\n📝 Ending section:")
        print(repr(ending_section))
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

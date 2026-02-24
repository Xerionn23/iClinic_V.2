import re
import os

student_files = [
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-dashboard.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-health-records.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-Announcement.html',
    r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-consulatation-chat.html'
]

logout_modal_html = '''
    <!-- Logout Confirmation Modal -->
    <div x-show="showLogoutConfirm" x-cloak
         x-transition:enter="transition ease-out duration-300"
         x-transition:enter-start="opacity-0"
         x-transition:enter-end="opacity-100"
         x-transition:leave="transition ease-in duration-200"
         x-transition:leave-start="opacity-100"
         x-transition:leave-end="opacity-0"
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
         @click.self="showLogoutConfirm = false">
        <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
            <div class="p-6">
                <div class="flex items-center mb-4">
                    <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
                        <i data-feather="log-out" class="w-5 h-5 text-red-600"></i>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-900">Confirm Logout</h3>
                </div>
                
                <p class="text-gray-600 mb-6">Are you sure you want to logout? You will need to login again to access the system.</p>
                
                <div class="flex justify-end space-x-3">
                    <button @click="showLogoutConfirm = false"
                            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
                        Cancel
                    </button>
                    <a href="{{ url_for('logout') }}"
                       class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 inline-block text-center">
                        Yes, Logout
                    </a>
                </div>
            </div>
        </div>
    </div>
'''

print("🔧 Adding logout confirmation modal to student pages...\n")

updated_count = 0

for file_path in student_files:
    try:
        filename = os.path.basename(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if already has logout modal
        if 'showLogoutConfirm' in content and 'Confirm Logout' in content:
            print(f"⚠️  {filename} - Already has logout modal")
            continue
        
        # Step 1: Add showLogoutConfirm variable to Alpine data
        if 'showLogoutConfirm' not in content:
            # For consultation chat (function-based)
            if 'function consultationChat()' in content:
                pattern = r"(return \{[\s\S]*?showNurseInfo: false,)"
                replacement = r"\1\n    showLogoutConfirm: false,"
                content = re.sub(pattern, replacement, content, count=1)
            else:
                # For inline x-data
                pattern = r"(x-data=\"\{[\s\S]*?profileDropdown: false,)"
                replacement = r"\1\n    showLogoutConfirm: false,"
                content = re.sub(pattern, replacement, content, count=1)
        
        # Step 2: Change logout link to button with modal trigger
        pattern_logout = r'<a href="\{\{ url_for\(\'logout\'\) \}\}"[^>]*>[\s\S]*?<span>Logout</span>[\s\S]*?</a>'
        replacement_logout = '''<button @click="showLogoutConfirm = true; profileDropdown = false" class="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors">
                        <i data-feather="log-out" class="w-4 h-4 text-red-600"></i>
                        <span>Logout</span>
                    </button>'''
        content = re.sub(pattern_logout, replacement_logout, content)
        
        # Step 3: Add modal before </body>
        if 'Confirm Logout' not in content:
            content = content.replace('</body>', logout_modal_html + '\n</body>')
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename} - Added logout modal")
            updated_count += 1
        else:
            print(f"⚠️  {filename} - No changes made")
            
    except Exception as e:
        print(f"❌ Error processing {filename}: {str(e)}")

print(f"\n✨ Complete! Updated {updated_count}/{len(student_files)} files")
print("\n📋 What was added:")
print("   - showLogoutConfirm variable to Alpine data")
print("   - Changed logout link to button with modal trigger")
print("   - Added logout confirmation modal")
print("\n✅ Result:")
print("   - Logout now shows confirmation modal")
print("   - Matches Nurse UI design")
print("   - Prevents accidental logout")

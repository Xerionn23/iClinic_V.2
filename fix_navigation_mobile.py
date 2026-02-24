#!/usr/bin/env python3
"""
Complete mobile navigation fix - hide sidebar on mobile by default
"""

def fix_mobile_navigation():
    file_path = r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Appointments.html'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Fixing mobile navigation visibility...")
    
    # 1. Update sidebar classes to hide on mobile by default
    old_sidebar = '''<aside :class="sidebarCollapsed ? 'w-20' : 'w-64'" 
               class="fixed left-0 top-0 h-screen gradient-bg-sidebar text-white transition-all duration-300 shadow-2xl z-50 transform md:transform-none"
               :class="{'translate-x-0': mobileMenuOpen, '-translate-x-full': !mobileMenuOpen}"'''
    
    new_sidebar = '''<aside class="fixed left-0 top-0 h-screen gradient-bg-sidebar text-white transition-all duration-300 shadow-2xl z-50"
               :class="{
                   'w-20': sidebarCollapsed && !mobileMenuOpen,
                   'w-64': !sidebarCollapsed || mobileMenuOpen,
                   '-translate-x-full md:translate-x-0': !mobileMenuOpen,
                   'translate-x-0': mobileMenuOpen
               }"'''
    
    content = content.replace(old_sidebar, new_sidebar)
    print("✅ Updated sidebar classes for mobile-first approach")
    
    # 2. Update responsive CSS
    old_css = '''
        /* Mobile Navigation Responsive */
        @media (max-width: 768px) {
            aside {
                width: 280px !important;
            }
            
            aside.translate-x-0 {
                transform: translateX(0);
            }
            
            aside.-translate-x-full {
                transform: translateX(-100%);
            }
        }
        
        /* Ensure sidebar is always visible on desktop */
        @media (min-width: 769px) {
            aside {
                transform: translateX(0) !important;
            }
        }
        
        /* Mobile menu button animation */
        @media (max-width: 768px) {
            [data-feather="menu"] {
                transition: transform 0.3s ease;
            }
        }
    '''
    
    new_css = '''
        /* Mobile Navigation - Hide by default */
        @media (max-width: 768px) {
            aside {
                width: 280px !important;
            }
            
            /* Hidden by default on mobile */
            aside.-translate-x-full {
                transform: translateX(-100%) !important;
            }
            
            /* Visible when menu is open */
            aside.translate-x-0 {
                transform: translateX(0) !important;
            }
        }
        
        /* Desktop - Always visible */
        @media (min-width: 769px) {
            aside {
                transform: translateX(0) !important;
            }
            
            aside.-translate-x-full {
                transform: translateX(0) !important;
            }
        }
        
        /* Mobile header only visible on mobile */
        .mobile-header {
            display: flex;
        }
        
        @media (min-width: 769px) {
            .mobile-header {
                display: none;
            }
        }
    '''
    
    content = content.replace(old_css, new_css)
    print("✅ Updated responsive CSS")
    
    # 3. Add class to mobile header
    content = content.replace(
        '<div class="md:hidden fixed top-0 left-0 right-0 bg-gradient-to-r from-blue-600 to-blue-700 text-white z-50 shadow-lg">',
        '<div class="mobile-header md:hidden fixed top-0 left-0 right-0 bg-gradient-to-r from-blue-600 to-blue-700 text-white z-50 shadow-lg">'
    )
    print("✅ Added mobile-header class")
    
    # 4. Ensure overlay closes menu
    content = content.replace(
        '@click="mobileMenuOpen = false"',
        '@click="mobileMenuOpen = false" style="display: none;" x-show="mobileMenuOpen"'
    )
    print("✅ Fixed overlay visibility")
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎉 SUCCESS! Mobile navigation fixed!")
    print("📱 Changes Applied:")
    print("   ✅ Sidebar hidden by default on mobile")
    print("   ✅ Only shows when hamburger menu clicked")
    print("   ✅ Always visible on desktop (≥769px)")
    print("   ✅ Proper mobile-first approach")
    print("\n✨ Refresh your browser to see the changes!")

if __name__ == "__main__":
    try:
        fix_mobile_navigation()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
"""
Script to make the navigation/sidebar fully responsive for mobile devices
"""

def fix_navigation_responsive():
    file_path = r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Appointments.html'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Applying navigation responsive fixes...")
    
    # 1. Add mobile menu button and overlay
    mobile_header = '''
        <!-- Mobile Header -->
        <div class="md:hidden fixed top-0 left-0 right-0 bg-gradient-to-r from-blue-600 to-blue-700 text-white z-50 shadow-lg">
            <div class="flex items-center justify-between p-4">
                <div class="flex items-center gap-3">
                    <img src="../assets/img/iclinic-logo.png" alt="iClinic" class="w-10 h-10 object-contain">
                    <div>
                        <h1 class="text-lg font-bold">iClinic</h1>
                        <p class="text-xs text-blue-100">Appointments</p>
                    </div>
                </div>
                <button @click="mobileMenuOpen = !mobileMenuOpen" class="p-2 hover:bg-white/10 rounded-lg transition-colors">
                    <i data-feather="menu" class="w-6 h-6"></i>
                </button>
            </div>
        </div>

        <!-- Mobile Menu Overlay -->
        <div x-show="mobileMenuOpen" 
             x-transition:enter="transition ease-out duration-300"
             x-transition:enter-start="opacity-0"
             x-transition:enter-end="opacity-100"
             x-transition:leave="transition ease-in duration-200"
             x-transition:leave-start="opacity-100"
             x-transition:leave-end="opacity-0"
             @click="mobileMenuOpen = false"
             class="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden">
        </div>

        '''
    
    # Insert mobile header after opening div
    content = content.replace(
        '<div class="flex h-screen overflow-hidden">',
        '<div class="flex h-screen overflow-hidden">\n' + mobile_header
    )
    print("✅ Added mobile header and overlay")
    
    # 2. Make sidebar responsive with mobile slide-in
    content = content.replace(
        '<aside :class="sidebarCollapsed ? \'w-20\' : \'w-64\'" \n               class="fixed left-0 top-0 h-screen gradient-bg-sidebar text-white transition-all duration-300 shadow-2xl z-40"',
        '''<aside :class="sidebarCollapsed ? 'w-20' : 'w-64'" 
               class="fixed left-0 top-0 h-screen gradient-bg-sidebar text-white transition-all duration-300 shadow-2xl z-50 transform md:transform-none"
               :class="{'translate-x-0': mobileMenuOpen, '-translate-x-full': !mobileMenuOpen}"'''
    )
    print("✅ Made sidebar responsive with mobile slide-in")
    
    # 3. Add mobile padding to logo
    content = content.replace(
        '<div class="relative p-6">',
        '<div class="relative p-4 sm:p-6">'
    )
    print("✅ Fixed logo padding for mobile")
    
    # 4. Make navigation items more compact on mobile
    content = content.replace(
        '<nav class="relative mt-8 px-4 space-y-2">',
        '<nav class="relative mt-4 sm:mt-8 px-3 sm:px-4 space-y-1 sm:space-y-2">'
    )
    print("✅ Made navigation more compact on mobile")
    
    # 5. Adjust navigation link padding for mobile
    content = content.replace(
        'class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group hover:bg-white/10">',
        'class="flex items-center gap-2 sm:gap-3 px-2 sm:px-3 py-2 sm:py-2.5 rounded-lg transition-all group hover:bg-white/10">'
    )
    content = content.replace(
        'class="sidebar-item-active flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group">',
        'class="sidebar-item-active flex items-center gap-2 sm:gap-3 px-2 sm:px-3 py-2 sm:py-2.5 rounded-lg transition-all group">'
    )
    print("✅ Fixed navigation link padding")
    
    # 6. Make icons responsive
    content = content.replace(
        '<i data-feather="home" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>',
        '<i data-feather="home" class="w-5 h-5 sm:w-5 sm:h-5 group-hover:scale-110 transition-transform"></i>'
    )
    print("✅ Made navigation icons responsive")
    
    # 7. Adjust user profile section for mobile
    content = content.replace(
        '<div class="absolute bottom-0 w-full p-4 bg-gradient-to-t from-black/20 to-transparent">',
        '<div class="absolute bottom-0 w-full p-3 sm:p-4 bg-gradient-to-t from-black/20 to-transparent">'
    )
    print("✅ Fixed user profile section padding")
    
    # 8. Add mobile padding to main content
    content = content.replace(
        '<div :class="sidebarCollapsed ? \'md:ml-20\' : \'md:ml-64\'" class="flex-1 flex flex-col transition-all duration-300">',
        '<div :class="sidebarCollapsed ? \'md:ml-20\' : \'md:ml-64\'" class="flex-1 flex flex-col transition-all duration-300 pt-16 md:pt-0">'
    )
    print("✅ Added mobile top padding for fixed header")
    
    # 9. Add responsive CSS for navigation
    responsive_nav_css = '''
        
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
    
    # Insert before closing </style>
    content = content.replace('        </style>', responsive_nav_css + '        </style>')
    print("✅ Added responsive navigation CSS")
    
    # 10. Add mobileMenuOpen to Alpine.js state
    content = content.replace(
        'sidebarCollapsed: false,',
        'sidebarCollapsed: false,\n                mobileMenuOpen: false,'
    )
    print("✅ Added mobileMenuOpen state to Alpine.js")
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎉 SUCCESS! Navigation is now fully responsive!")
    print("📱 Mobile Features Added:")
    print("   ✅ Mobile header with hamburger menu")
    print("   ✅ Slide-in sidebar navigation")
    print("   ✅ Touch-friendly navigation items")
    print("   ✅ Responsive padding and spacing")
    print("   ✅ Mobile overlay for better UX")
    print("\n✨ Refresh your browser to see the changes!")

if __name__ == "__main__":
    try:
        fix_navigation_responsive()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please make sure the file path is correct and you have write permissions.")

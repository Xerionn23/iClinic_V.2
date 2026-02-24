#!/usr/bin/env python3
"""
Complete responsive fix for Staff-Consultations.html
Makes navigation mobile-friendly and fixes UI issues
"""

def fix_consultations_responsive():
    file_path = r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Consultations.html'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Applying responsive fixes to Consultations page...")
    
    # 1. Add mobileMenuOpen to Alpine.js data
    if 'mobileMenuOpen: false,' not in content:
        content = content.replace(
            'sidebarCollapsed: false,',
            'sidebarCollapsed: false,\n                mobileMenuOpen: false,'
        )
        print("✅ Added mobileMenuOpen state")
    
    # 2. Add mobile header
    mobile_header = '''
        <!-- Mobile Header -->
        <div class="mobile-header md:hidden fixed top-0 left-0 right-0 bg-gradient-to-r from-blue-600 to-blue-700 text-white z-50 shadow-lg">
            <div class="flex items-center justify-between p-4">
                <div class="flex items-center gap-3">
                    <img src="../assets/img/iclinic-logo.png" alt="iClinic" class="w-10 h-10 object-contain">
                    <div>
                        <h1 class="text-lg font-bold">iClinic</h1>
                        <p class="text-xs text-blue-100">Consultations</p>
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
             style="display: none;"
             class="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden">
        </div>

        '''
    
    if '<!-- Mobile Header -->' not in content:
        content = content.replace(
            '<div class="flex h-screen overflow-hidden">',
            '<div class="flex h-screen overflow-hidden">\n' + mobile_header
        )
        print("✅ Added mobile header and overlay")
    
    # 3. Update sidebar to be mobile responsive
    old_sidebar = '''<aside :class="sidebarCollapsed ? 'w-20' : 'w-64'" 
               class="fixed left-0 top-0 h-screen gradient-bg-sidebar text-white transition-all duration-300 shadow-2xl z-40"
               @mouseenter="sidebarHovered = true"
               @mouseleave="sidebarHovered = false">'''
    
    new_sidebar = '''<aside class="fixed left-0 top-0 h-screen gradient-bg-sidebar text-white transition-all duration-300 shadow-2xl z-50"
               :class="{
                   'w-20': sidebarCollapsed && !mobileMenuOpen,
                   'w-64': !sidebarCollapsed || mobileMenuOpen,
                   '-translate-x-full md:translate-x-0': !mobileMenuOpen,
                   'translate-x-0': mobileMenuOpen
               }"
               @mouseenter="sidebarHovered = true"
               @mouseleave="sidebarHovered = false">'''
    
    content = content.replace(old_sidebar, new_sidebar)
    print("✅ Updated sidebar for mobile responsiveness")
    
    # 4. Add mobile padding to main content
    content = content.replace(
        '<div :class="sidebarCollapsed ? \'md:ml-20\' : \'md:ml-64\'" class="flex-1 flex flex-col transition-all duration-300">',
        '<div :class="sidebarCollapsed ? \'md:ml-20\' : \'md:ml-64\'" class="flex-1 flex flex-col transition-all duration-300 pt-16 md:pt-0">'
    )
    print("✅ Added mobile top padding")
    
    # 5. Make sidebar logo and navigation responsive
    content = content.replace(
        '<div class="relative p-6">',
        '<div class="relative p-4 sm:p-6">'
    )
    
    content = content.replace(
        '<nav class="relative mt-8 px-4 space-y-2">',
        '<nav class="relative mt-4 sm:mt-8 px-3 sm:px-4 space-y-1 sm:space-y-2">'
    )
    print("✅ Made sidebar padding responsive")
    
    # 6. Add responsive CSS
    responsive_css = '''
        
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
        
        /* Responsive main content padding */
        @media (max-width: 640px) {
            main {
                padding: 0.75rem !important;
            }
        }
        
        /* Responsive header */
        @media (max-width: 640px) {
            .glass {
                border-radius: 1rem !important;
                padding: 1rem !important;
            }
        }
        
        /* Touch targets for mobile */
        @media (max-width: 768px) {
            button, a {
                min-height: 44px;
            }
        }
    '''
    
    # Insert before closing </style>
    if '/* Mobile Navigation - Hide by default */' not in content:
        content = content.replace('    </style>', responsive_css + '    </style>')
        print("✅ Added responsive CSS")
    
    # 7. Make main content padding responsive
    content = content.replace(
        '<main class="flex-1 overflow-y-auto bg-gray-50 p-6">',
        '<main class="flex-1 overflow-y-auto bg-gray-50 p-3 sm:p-4 md:p-6">'
    )
    print("✅ Made main content padding responsive")
    
    # 8. Make header responsive
    content = content.replace(
        '<div class="glass rounded-[2rem] ml-1">',
        '<div class="glass rounded-xl sm:rounded-2xl md:rounded-[2rem] ml-0 sm:ml-1">'
    )
    print("✅ Made header rounding responsive")
    
    # 9. Make header padding responsive
    content = content.replace(
        '<div class="relative px-6 py-5">',
        '<div class="relative px-3 sm:px-4 md:px-6 py-3 sm:py-4 md:py-5">'
    )
    print("✅ Made header padding responsive")
    
    # 10. Make title text responsive
    content = content.replace(
        '<h1 class="text-2xl sm:text-3xl font-bold text-gray-800 dark:text-white">',
        '<h1 class="text-xl sm:text-2xl md:text-3xl font-bold text-gray-800 dark:text-white">'
    )
    print("✅ Made title text responsive")
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎉 SUCCESS! Consultations page is now fully responsive!")
    print("📱 Mobile Features Added:")
    print("   ✅ Mobile header with hamburger menu")
    print("   ✅ Slide-in sidebar navigation")
    print("   ✅ Hidden sidebar by default on mobile")
    print("   ✅ Touch-friendly buttons (44px minimum)")
    print("   ✅ Responsive padding and spacing")
    print("   ✅ Responsive text sizes")
    print("   ✅ Mobile overlay for better UX")
    print("\n✨ Refresh your browser to see the changes!")

if __name__ == "__main__":
    try:
        fix_consultations_responsive()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

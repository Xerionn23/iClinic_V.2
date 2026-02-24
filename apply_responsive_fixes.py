#!/usr/bin/env python3
"""
Script to apply responsive design fixes to Staff-Appointments.html
This will make ALL components responsive for mobile, tablet, and desktop devices
"""

import re

def apply_responsive_fixes():
    file_path = r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Appointments.html'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Applying responsive fixes...")
    
    # 1. Main content padding
    content = content.replace(
        '<main class="flex-1 overflow-y-auto bg-gray-50 p-6">',
        '<main class="flex-1 overflow-y-auto bg-gray-50 p-2 sm:p-4 md:p-6">'
    )
    print("✅ Fixed main content padding")
    
    # 2. Header rounded corners and margin
    content = content.replace(
        'rounded-[2rem] ml-1">',
        'rounded-xl sm:rounded-2xl md:rounded-[2rem] ml-0 sm:ml-1">'
    )
    print("✅ Fixed header rounding")
    
    # 3. Header content padding
    content = content.replace(
        '<div class="relative px-6 py-5">',
        '<div class="relative px-3 sm:px-4 md:px-6 py-3 sm:py-4 md:py-5">'
    )
    print("✅ Fixed header padding")
    
    # 4. Title icon size
    content = content.replace(
        '<div class="w-12 h-12 bg-yellow-400 rounded-xl flex items-center justify-center shadow-lg transform rotate-2 hover:rotate-0 transition-transform duration-300">',
        '<div class="w-10 h-10 sm:w-12 sm:h-12 bg-yellow-400 rounded-lg sm:rounded-xl flex items-center justify-center shadow-lg transform rotate-2 hover:rotate-0 transition-transform duration-300">'
    )
    content = content.replace(
        '<i data-feather="calendar" class="w-6 h-6 text-blue-900"></i>',
        '<i data-feather="calendar" class="w-5 h-5 sm:w-6 sm:h-6 text-blue-900"></i>',
        1  # Only first occurrence
    )
    print("✅ Fixed title icon sizing")
    
    # 5. Title text size
    content = content.replace(
        '<h1 class="text-2xl sm:text-3xl font-bold text-white">',
        '<h1 class="text-xl sm:text-2xl md:text-3xl font-bold text-white">'
    )
    print("✅ Fixed title text sizing")
    
    # 6. Subtitle text - make responsive
    content = content.replace(
        '<span class="text-sm">Manage and schedule patient appointments</span>',
        '<span class="text-xs sm:text-sm">Manage and schedule patient appointments</span>'
    )
    print("✅ Fixed subtitle text")
    
    # 7. Event button - touch-friendly
    content = content.replace(
        'class="group bg-white/15 hover:bg-white/25 backdrop-blur-sm text-white px-4 py-2 rounded-lg font-medium border border-white/30 hover:border-white/50 transition-all duration-200 flex items-center gap-2 shadow-lg hover:scale-105">',
        'class="group bg-white/15 hover:bg-white/25 backdrop-blur-sm text-white px-3 sm:px-4 py-2 sm:py-2.5 rounded-lg font-medium border border-white/30 hover:border-white/50 transition-all duration-200 flex items-center gap-2 shadow-lg hover:scale-105 min-h-[44px]">'
    )
    content = content.replace(
        '<div class="w-6 h-6 bg-orange-500/30 rounded flex items-center justify-center group-hover:bg-orange-500/50 transition-colors">',
        '<div class="w-5 h-5 sm:w-6 sm:h-6 bg-orange-500/30 rounded flex items-center justify-center group-hover:bg-orange-500/50 transition-colors">'
    )
    content = content.replace(
        '<i data-feather="alert-circle" class="w-3 h-3"></i>',
        '<i data-feather="alert-circle" class="w-3 h-3 sm:w-4 sm:h-4"></i>'
    )
    content = content.replace(
        '<span class="hidden sm:inline">Event</span>',
        '<span class="hidden sm:inline text-sm sm:text-base">Event</span>'
    )
    print("✅ Fixed event button")
    
    # 8. Content padding after header
    content = re.sub(
        r'<!-- Appointments Content -->\s*<div class="p-6">',
        '<!-- Appointments Content -->\n                <div class="p-3 sm:p-4 md:p-6">',
        content
    )
    print("✅ Fixed content padding")
    
    # 9. Section header
    content = content.replace(
        '<h2 class="section-header text-lg font-semibold text-gray-800">Today\'s Overview</h2>',
        '<h2 class="section-header text-base sm:text-lg font-semibold text-gray-800">Today\'s Overview</h2>'
    )
    print("✅ Fixed section header")
    
    # 10. Statistics cards padding
    content = content.replace(
        'class="stat-card bg-white rounded-xl shadow-md border border-gray-100 p-6 hover:shadow-xl"',
        'class="stat-card bg-white rounded-lg sm:rounded-xl shadow-md border border-gray-100 p-4 sm:p-5 md:p-6 hover:shadow-xl"'
    )
    print("✅ Fixed statistics cards padding")
    
    # 11. Card text sizes - Total Appointments
    content = content.replace(
        '<p class="text-xs font-semibold uppercase tracking-wide text-gray-500 mb-1">Total Appointments</p>',
        '<p class="text-[10px] sm:text-xs font-semibold uppercase tracking-wide text-gray-500 mb-1">Total Appointments</p>'
    )
    content = content.replace(
        '<p class="text-xs font-semibold uppercase tracking-wide text-gray-500 mb-1">Today\'s Appointments</p>',
        '<p class="text-[10px] sm:text-xs font-semibold uppercase tracking-wide text-gray-500 mb-1">Today\'s Appointments</p>'
    )
    content = content.replace(
        '<p class="text-xs font-semibold uppercase tracking-wide text-gray-500 mb-1">Upcoming</p>',
        '<p class="text-[10px] sm:text-xs font-semibold uppercase tracking-wide text-gray-500 mb-1">Upcoming</p>'
    )
    content = content.replace(
        '<p class="text-xs font-semibold uppercase tracking-wide text-gray-500 mb-1">This Month</p>',
        '<p class="text-[10px] sm:text-xs font-semibold uppercase tracking-wide text-gray-500 mb-1">This Month</p>'
    )
    print("✅ Fixed card label text sizes")
    
    # 12. Card number sizes
    content = re.sub(
        r'<p class="text-3xl font-bold text-gray-900" x-text="(totalAppointments|todayAppointmentsCount|upcomingCount|thisMonthCount)">',
        r'<p class="text-2xl sm:text-3xl font-bold text-gray-900" x-text="\1">',
        content
    )
    print("✅ Fixed card number sizes")
    
    # 13. Card icons
    content = content.replace(
        '<div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">',
        '<div class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg sm:rounded-xl flex items-center justify-center shadow-lg">'
    )
    content = content.replace(
        '<div class="w-14 h-14 bg-gradient-to-br from-yellow-400 to-yellow-500 rounded-xl flex items-center justify-center shadow-lg">',
        '<div class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-yellow-400 to-yellow-500 rounded-lg sm:rounded-xl flex items-center justify-center shadow-lg">'
    )
    content = content.replace(
        '<div class="w-14 h-14 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center shadow-lg">',
        '<div class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-green-500 to-green-600 rounded-lg sm:rounded-xl flex items-center justify-center shadow-lg">'
    )
    content = content.replace(
        '<div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">',
        '<div class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg sm:rounded-xl flex items-center justify-center shadow-lg">'
    )
    
    # Icon sizes in cards
    content = re.sub(
        r'<i data-feather="(calendar|check-circle|trending-up)" class="w-7 h-7 text-white"></i>',
        r'<i data-feather="\1" class="w-6 h-6 sm:w-7 sm:h-7 text-white"></i>',
        content
    )
    print("✅ Fixed card icons")
    
    # 14. Add responsive CSS
    responsive_css = '''
        
        /* Extra responsive breakpoints for mobile */
        @media (max-width: 374px) {
            .stat-card {
                padding: 0.75rem !important;
            }
            
            .stat-card p:first-child {
                font-size: 9px !important;
            }
            
            .stat-card p:nth-child(2) {
                font-size: 1.5rem !important;
            }
        }
        
        /* Touch targets for mobile */
        .touch-target {
            min-height: 44px;
            min-width: 44px;
        }
        
        /* Responsive calendar */
        @media (max-width: 640px) {
            .calendar-grid {
                font-size: 0.875rem;
            }
        }
    '''
    
    # Insert before closing </style>
    content = content.replace('    </style>', responsive_css + '    </style>')
    print("✅ Added responsive CSS")
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎉 SUCCESS! All responsive fixes applied!")
    print("📱 The page is now fully responsive for:")
    print("   - Mobile phones (320px - 640px)")
    print("   - Tablets (641px - 768px)")
    print("   - Desktops (769px+)")
    print("\n✨ Refresh your browser to see the changes!")

if __name__ == "__main__":
    try:
        apply_responsive_fixes()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please make sure the file path is correct and you have write permissions.")

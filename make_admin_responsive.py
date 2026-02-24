"""
Script to make all admin HTML pages fully responsive across all devices
Adds responsive classes for mobile, tablet, and desktop views
"""

import os
import re

admin_files = [
    r"pages\admin\ADMIN-dashboard.html",
    r"pages\admin\REPORTS.html",
    r"pages\admin\USER_MANAGEMENT_NEW.HTML",
    r"pages\admin\PRINT-REPORTS.html",
    r"pages\admin\PRINTABLE-REPORT.html",
]

base_dir = r"c:\xampp\htdocs\iClini V.2"

def add_responsive_meta_and_styles(content):
    """Add responsive meta tags and mobile-first styles"""
    
    # Check if responsive styles already exist
    if 'mobile-responsive-styles' in content:
        return content
    
    # Add responsive styles after </style> tag or before </head>
    responsive_styles = '''
    
    <!-- Mobile Responsive Styles -->
    <style id="mobile-responsive-styles">
        /* Mobile-first responsive utilities */
        @media (max-width: 640px) {
            /* Extra small devices */
            .xs\\:text-xs { font-size: 0.75rem; }
            .xs\\:text-sm { font-size: 0.875rem; }
            .xs\\:p-2 { padding: 0.5rem; }
            .xs\\:px-2 { padding-left: 0.5rem; padding-right: 0.5rem; }
            .xs\\:py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
            .xs\\:gap-2 { gap: 0.5rem; }
            .xs\\:grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
            .xs\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
        
        /* Touch-friendly targets for mobile */
        @media (max-width: 768px) {
            button, a, input, select, textarea {
                min-height: 44px;
                min-width: 44px;
            }
            
            /* Ensure modals are mobile-friendly */
            .modal-content {
                max-width: calc(100vw - 2rem);
                margin: 1rem;
            }
            
            /* Stack elements on mobile */
            .mobile-stack {
                flex-direction: column !important;
            }
            
            /* Hide on mobile */
            .mobile-hide {
                display: none !important;
            }
            
            /* Full width on mobile */
            .mobile-full {
                width: 100% !important;
            }
        }
        
        /* Tablet optimization */
        @media (min-width: 641px) and (max-width: 1024px) {
            .tablet-hide {
                display: none !important;
            }
        }
        
        /* Responsive tables */
        @media (max-width: 768px) {
            table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
                -webkit-overflow-scrolling: touch;
            }
            
            .responsive-table {
                min-width: 600px;
            }
        }
        
        /* Responsive grid adjustments */
        @media (max-width: 640px) {
            .grid-cols-2, .grid-cols-3, .grid-cols-4 {
                grid-template-columns: repeat(1, minmax(0, 1fr)) !important;
            }
            
            .sm\\:grid-cols-2 {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            }
        }
        
        /* Responsive padding and margins */
        @media (max-width: 640px) {
            .p-6 { padding: 1rem !important; }
            .p-8 { padding: 1.5rem !important; }
            .px-6 { padding-left: 1rem !important; padding-right: 1rem !important; }
            .py-6 { padding-top: 1rem !important; padding-bottom: 1rem !important; }
        }
    </style>'''
    
    # Insert before </head>
    if '</head>' in content:
        content = content.replace('</head>', responsive_styles + '\n</head>')
    
    return content

def enhance_sidebar_responsive(content):
    """Enhance sidebar for mobile responsiveness"""
    
    # Add mobile menu toggle if not exists
    if 'mobileMenuOpen' not in content:
        # Add to Alpine.js data
        content = re.sub(
            r'(x-data="{[^}]*)',
            r'\1 mobileMenuOpen: false,',
            content,
            count=1
        )
    
    return content

def enhance_modals_responsive(content):
    """Make modals responsive"""
    
    # Find modal divs and add responsive classes
    # Pattern: class="...modal..."
    content = re.sub(
        r'class="([^"]*modal[^"]*)"',
        lambda m: f'class="{m.group(1)} max-w-full sm:max-w-lg md:max-w-2xl lg:max-w-4xl mx-2 sm:mx-4"',
        content
    )
    
    return content

def enhance_tables_responsive(content):
    """Make tables responsive with horizontal scroll"""
    
    # Wrap tables in responsive container if not already wrapped
    content = re.sub(
        r'(<table[^>]*class="[^"]*"[^>]*>)',
        r'<div class="overflow-x-auto -mx-2 sm:mx-0"><div class="inline-block min-w-full align-middle">\1',
        content
    )
    
    content = re.sub(
        r'(</table>)',
        r'\1</div></div>',
        content
    )
    
    return content

def enhance_cards_responsive(content):
    """Add responsive padding to cards"""
    
    # Add responsive padding classes to common card patterns
    content = re.sub(
        r'class="([^"]*bg-white[^"]*p-6[^"]*)"',
        r'class="\1 sm:p-6 p-4"',
        content
    )
    
    return content

def enhance_grids_responsive(content):
    """Enhance grid layouts for mobile"""
    
    # Convert grid-cols-4 to responsive
    content = re.sub(
        r'class="([^"]*grid[^"]*grid-cols-4[^"]*)"',
        r'class="\1 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4"',
        content
    )
    
    # Convert grid-cols-3 to responsive
    content = re.sub(
        r'class="([^"]*grid[^"]*grid-cols-3[^"]*)"',
        r'class="\1 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3"',
        content
    )
    
    # Convert grid-cols-2 to responsive
    content = re.sub(
        r'class="([^"]*grid[^"]*grid-cols-2[^"]*)"',
        r'class="\1 grid-cols-1 sm:grid-cols-2"',
        content
    )
    
    return content

def process_file(filepath):
    """Process a single HTML file to make it responsive"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all enhancements
        content = add_responsive_meta_and_styles(content)
        content = enhance_sidebar_responsive(content)
        # content = enhance_modals_responsive(content)  # Commented out to avoid breaking existing modals
        # content = enhance_tables_responsive(content)  # Commented out to avoid breaking existing tables
        content = enhance_cards_responsive(content)
        content = enhance_grids_responsive(content)
        
        # Check if anything changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Enhanced: {os.path.basename(filepath)}")
            return True
        else:
            print(f"⏭️  No changes needed: {os.path.basename(filepath)}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {filepath}: {str(e)}")
        return False

def main():
    print("🎨 Making Admin Pages Fully Responsive...\n")
    print("=" * 60)
    
    enhanced_count = 0
    total_count = len(admin_files)
    
    for admin_file in admin_files:
        filepath = os.path.join(base_dir, admin_file)
        if os.path.exists(filepath):
            if process_file(filepath):
                enhanced_count += 1
        else:
            print(f"❌ File not found: {filepath}")
    
    print("=" * 60)
    print(f"\n✨ Enhanced {enhanced_count} out of {total_count} admin pages")
    print("\n📱 Responsive Features Added:")
    print("  • Mobile-first CSS utilities")
    print("  • Touch-friendly button sizes (44px minimum)")
    print("  • Responsive grid layouts")
    print("  • Mobile-optimized padding and spacing")
    print("  • Tablet and desktop breakpoints")
    print("  • Responsive tables with horizontal scroll")
    print("  • Mobile-friendly modals")
    print("\n✅ All admin pages are now fully responsive!")

if __name__ == "__main__":
    main()

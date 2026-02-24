# PowerShell script to remove extra navigation items
# Keep only Health Reports and Consultation Chat

$filePath = 'c:\xampp\htdocs\iClini V.2\pages\deans_president\Deans_consultationchat.html'

Write-Host "Reading file..." -ForegroundColor Cyan
$lines = Get-Content $filePath

Write-Host "Processing navigation section..." -ForegroundColor Cyan

$newLines = @()
$skipMode = $false
$navStartFound = $false

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    
    # Detect navigation start
    if ($line -match '<!-- Navigation -->') {
        $navStartFound = $true
        $newLines += $line
        $newLines += $lines[$i+1]  # <nav> tag
        
        # Add Health Reports
        $newLines += '                <!-- Health Reports -->'
        $newLines += '                <a href="{{ url_for(''deans_president_dashboard'') }}"'
        $newLines += '                   class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all group hover:bg-white/10">'
        $newLines += '                    <div class="flex items-center justify-center" :class="sidebarCollapsed && !sidebarHovered ? ''w-full'' : ''''">
        $newLines += '                        <i data-feather="activity" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>'
        $newLines += '                    </div>'
        $newLines += '                    <span x-show="!sidebarCollapsed || sidebarHovered" x-transition class="font-medium">Health Reports</span>'
        $newLines += '                </a>'
        $newLines += '                '
        
        # Skip to Consultation Chat section
        $skipMode = $true
        $i++  # Skip the <nav> line we already added
        continue
    }
    
    # When we find Consultation Chat, stop skipping
    if ($skipMode -and $line -match '<!-- Consultation Chat -->') {
        $skipMode = $false
        # Add Consultation Chat with correct route
        $newLines += '                <!-- Consultation Chat -->'
        $newLines += '                <a href="{{ url_for(''deans_president_consultation_chat'') }}"'
        $newLines += '                   class="sidebar-item-active flex items-center gap-3 px-4 py-3 rounded-lg transition-all group">'
        $newLines += '                    <div class="flex items-center justify-center" :class="sidebarCollapsed && !sidebarHovered ? ''w-full'' : ''''">
        $newLines += '                        <i data-feather="message-circle" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>'
        $newLines += '                    </div>'
        $newLines += '                    <span x-show="!sidebarCollapsed || sidebarHovered" x-transition class="font-medium">Consultation Chat</span>'
        $newLines += '                </a>'
        
        # Skip the old Consultation Chat lines
        while ($i -lt $lines.Count -and $lines[$i] -notmatch '</a>') {
            $i++
        }
        continue
    }
    
    # When we reach </nav>, stop skipping and add it
    if ($skipMode -and $line -match '</nav>') {
        $skipMode = $false
        $newLines += $line
        continue
    }
    
    # Skip lines between nav start and Consultation Chat
    if ($skipMode) {
        continue
    }
    
    # Add all other lines normally
    $newLines += $line
}

Write-Host "`nSaving changes..." -ForegroundColor Cyan
$newLines | Set-Content $filePath

Write-Host "`n✅ Navigation updated successfully!" -ForegroundColor Green
Write-Host "Removed: Dashboard, Health Records, Appointments, Announcements" -ForegroundColor Yellow
Write-Host "Kept: Health Reports and Consultation Chat" -ForegroundColor Green

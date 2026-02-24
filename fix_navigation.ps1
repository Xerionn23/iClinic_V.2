# PowerShell script to remove extra navigation items
# Keep only Health Reports and Consultation Chat

$filePath = 'c:\xampp\htdocs\iClini V.2\pages\deans_president\Deans_consultationchat.html'

Write-Host "Reading file..." -ForegroundColor Cyan
$content = Get-Content $filePath -Raw

Write-Host "Removing extra navigation items..." -ForegroundColor Cyan

# Find and replace the entire navigation section
$oldNav = @'
            <!-- Navigation -->
            <nav class="relative mt-8 px-4 space-y-3">
                <!-- Dashboard -->
                <a href="{{ url_for('student_dashboard') }}"
                   class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all group hover:bg-white/10">
                    <div class="flex items-center justify-center" :class="sidebarCollapsed && !sidebarHovered ? 'w-full' : ''">
                        <i data-feather="home" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>
                    </div>
                    <span x-show="!sidebarCollapsed || sidebarHovered" x-transition class="font-medium">Dashboard</span>
                </a>
                
                <!-- Health Records -->
                <a href="{{ url_for('student_health_records') }}"
                   class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all group hover:bg-white/10">
                    <div class="flex items-center justify-center" :class="sidebarCollapsed && !sidebarHovered ? 'w-full' : ''">
                        <i data-feather="file-text" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>
                    </div>
                    <span x-show="!sidebarCollapsed || sidebarHovered" x-transition class="font-medium">Health Records</span>
                </a>
                
                <!-- Appointments -->
                <a href="{{ url_for('student_appointments') }}"
                   class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all group hover:bg-white/10">
                    <div class="flex items-center justify-center" :class="sidebarCollapsed && !sidebarHovered ? 'w-full' : ''">
                        <i data-feather="calendar" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>
                    </div>
                    <span x-show="!sidebarCollapsed || sidebarHovered" x-transition class="font-medium">Appointments</span>
                </a>
                
                <!-- Consultation Chat -->
                <a href="{{ url_for('student_consultation_chat') }}"
                   class="sidebar-item-active flex items-center gap-3 px-4 py-3 rounded-lg transition-all group">
                    <div class="flex items-center justify-center" :class="sidebarCollapsed && !sidebarHovered ? 'w-full' : ''">
                        <i data-feather="message-circle" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>
                    </div>
                    <span x-show="!sidebarCollapsed || sidebarHovered" x-transition class="font-medium">Consultation Chat</span>
                </a>
                
                <!-- Announcements -->
                <a href="{{ url_for('student_announcements') }}"
                   class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all group hover:bg-white/10">
                    <div class="flex items-center justify-center" :class="sidebarCollapsed && !sidebarHovered ? 'w-full' : ''">
                        <i data-feather="volume-2" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>
                    </div>
                    <span x-show="!sidebarCollapsed || sidebarHovered" class="font-medium">Announcements</span>
                </a>
            </nav>
'@

$newNav = @'
            <!-- Navigation -->
            <nav class="relative mt-8 px-4 space-y-3">
                <!-- Health Reports -->
                <a href="{{ url_for('deans_president_dashboard') }}"
                   class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all group hover:bg-white/10">
                    <div class="flex items-center justify-center" :class="sidebarCollapsed && !sidebarHovered ? 'w-full' : ''">
                        <i data-feather="activity" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>
                    </div>
                    <span x-show="!sidebarCollapsed || sidebarHovered" x-transition class="font-medium">Health Reports</span>
                </a>
                
                <!-- Consultation Chat -->
                <a href="{{ url_for('deans_president_consultation_chat') }}"
                   class="sidebar-item-active flex items-center gap-3 px-4 py-3 rounded-lg transition-all group">
                    <div class="flex items-center justify-center" :class="sidebarCollapsed && !sidebarHovered ? 'w-full' : ''">
                        <i data-feather="message-circle" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>
                    </div>
                    <span x-show="!sidebarCollapsed || sidebarHovered" x-transition class="font-medium">Consultation Chat</span>
                </a>
            </nav>
'@

$content = $content -replace [regex]::Escape($oldNav), $newNav

Write-Host "`nSaving changes..." -ForegroundColor Cyan
Set-Content $filePath -Value $content -NoNewline

Write-Host "`n✅ Navigation updated successfully!" -ForegroundColor Green
Write-Host "Only Health Reports and Consultation Chat remain in navigation" -ForegroundColor Yellow

# Simple script to fix navigation - remove unwanted items

$filePath = 'c:\xampp\htdocs\iClini V.2\pages\deans_president\Deans_consultationchat.html'

Write-Host "Reading file..." -ForegroundColor Cyan
$content = Get-Content $filePath -Raw

Write-Host "Removing Dashboard navigation..." -ForegroundColor Yellow
# Remove Dashboard section (lines with Dashboard)
$content = $content -replace '(?s)<!-- Dashboard -->.*?</a>\s+(?=<!-- Health Records -->|<!-- Consultation Chat -->)', ''

Write-Host "Removing Health Records navigation..." -ForegroundColor Yellow
# Remove Health Records section
$content = $content -replace '(?s)<!-- Health Records -->.*?</a>\s+(?=<!-- Appointments -->|<!-- Consultation Chat -->)', ''

Write-Host "Removing Appointments navigation..." -ForegroundColor Yellow
# Remove Appointments section
$content = $content -replace '(?s)<!-- Appointments -->.*?</a>\s+(?=<!-- Consultation Chat -->)', ''

Write-Host "Removing Announcements navigation..." -ForegroundColor Yellow
# Remove Announcements section
$content = $content -replace '(?s)<!-- Announcements -->.*?</a>\s+(?=</nav>)', ''

Write-Host "Updating Consultation Chat route..." -ForegroundColor Cyan
# Fix Consultation Chat route
$content = $content -replace "url_for\('student_consultation_chat'\)", "url_for('deans_president_consultation_chat')"

Write-Host "Adding Health Reports navigation..." -ForegroundColor Green
# Add Health Reports before Consultation Chat
$healthReports = @'
                <!-- Health Reports -->
                <a href="{{ url_for('deans_president_dashboard') }}"
                   class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all group hover:bg-white/10">
                    <div class="flex items-center justify-center" :class="sidebarCollapsed && !sidebarHovered ? 'w-full' : ''">
                        <i data-feather="activity" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>
                    </div>
                    <span x-show="!sidebarCollapsed || sidebarHovered" x-transition class="font-medium">Health Reports</span>
                </a>
                
'@

$content = $content -replace '(\s+<!-- Consultation Chat -->)', "$healthReports`$1"

Write-Host "`nSaving changes..." -ForegroundColor Cyan
Set-Content $filePath -Value $content -NoNewline

Write-Host "`n✅ Navigation fixed successfully!" -ForegroundColor Green
Write-Host "Navigation now has: Health Reports and Consultation Chat only" -ForegroundColor Yellow

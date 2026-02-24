# Fix auto-consultation creation issue
# Don't create consultation automatically - only when user sends first message

$filePath = 'c:\xampp\htdocs\iClini V.2\pages\deans_president\Deans_consultationchat.html'

Write-Host "Reading file..." -ForegroundColor Cyan
$content = Get-Content $filePath -Raw

Write-Host "Disabling auto-consultation creation..." -ForegroundColor Yellow

# Comment out the initializeConsultation() call
$content = $content -replace '            // Check for existing consultation or start new one\r?\n            this.initializeConsultation\(\);', '            // Don''t auto-create consultation - only create when user sends first message
            // this.initializeConsultation();'

Write-Host "`nSaving changes..." -ForegroundColor Cyan
Set-Content $filePath -Value $content -NoNewline

Write-Host "`n✅ Fixed!" -ForegroundColor Green
Write-Host "Consultation will only be created when user sends first message" -ForegroundColor Yellow

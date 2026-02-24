# Fix Dean/President identification in consultation chat

$filePath = 'c:\xampp\htdocs\iClini V.2\pages\deans_president\Deans_consultationchat.html'

Write-Host "Reading file..." -ForegroundColor Cyan
$content = Get-Content $filePath -Raw

Write-Host "Updating patient_name..." -ForegroundColor Yellow
$content = $content -replace "patient_name: 'Current Student',", "patient_name: '{{ user.first_name }} {{ user.last_name }}',"

Write-Host "Updating patient_type..." -ForegroundColor Yellow
$content = $content -replace "patient_type: 'student',", "patient_type: '{{ user.role }}',"

Write-Host "Updating complaint message..." -ForegroundColor Yellow
$content = $content -replace "complaint: 'General consultation request - Student seeking healthcare assistance'", "complaint: 'General consultation request from {{ user.position or user.role }}'"

Write-Host "`nSaving changes..." -ForegroundColor Cyan
Set-Content $filePath -Value $content -NoNewline

Write-Host "`n✅ Fixed!" -ForegroundColor Green
Write-Host "Now uses actual user name and role from session" -ForegroundColor Yellow

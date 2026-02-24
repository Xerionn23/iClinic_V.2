# Fix Dean/President identification in consultation chat
# Update to use actual user info from session instead of hardcoded "Current Student"

$filePath = 'c:\xampp\htdocs\iClini V.2\pages\deans_president\Deans_consultationchat.html'

Write-Host "Reading file..." -ForegroundColor Cyan
$content = Get-Content $filePath -Raw

Write-Host "Updating consultation initialization..." -ForegroundColor Yellow

# Replace the hardcoded patient info with dynamic session-based info
$oldCode = @'
            body: JSON.stringify({
                patient_name: 'Current Student',  // Let backend determine from session
                patient_type: 'student',
                complaint: 'General consultation request - Student seeking healthcare assistance'
            })
'@

$newCode = @'
            body: JSON.stringify({
                patient_name: '{{ user.first_name }} {{ user.last_name }}',  // Use actual dean/president name
                patient_type: '{{ user.role }}',  // Use actual role (dean/president)
                complaint: 'General consultation request from {{ user.position or user.role }}'
            })
'@

$content = $content -replace [regex]::Escape($oldCode), $newCode

Write-Host "✓ Updated consultation initialization" -ForegroundColor Green

Write-Host "`nSaving changes..." -ForegroundColor Cyan
Set-Content $filePath -Value $content -NoNewline

Write-Host "`n✅ Dean/President identification fixed!" -ForegroundColor Green
Write-Host "Consultation will now use actual user name and role from session" -ForegroundColor Yellow

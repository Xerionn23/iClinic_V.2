# PowerShell script to UNDO changes - restore back to 'student'
# This script changes 'dean' references back to 'student'

$filePath = 'c:\xampp\htdocs\iClini V.2\pages\deans_president\Deans_consultationchat.html'

Write-Host "Reading file..." -ForegroundColor Cyan
$content = Get-Content $filePath -Raw

Write-Host "Making replacements..." -ForegroundColor Cyan

# UNDO Change 1: patient_type from dean back to student
$content = $content -replace 'patient_type: ''dean''', 'patient_type: ''student'''
Write-Host '✓ Restored patient_type to student' -ForegroundColor Green

# UNDO Change 2: sender mapping in loadMessages
$content = $content -replace "sender_type === 'patient' \? 'dean'", "sender_type === 'patient' ? 'student'"
Write-Host '✓ Restored message sender mapping to student' -ForegroundColor Green

# UNDO Change 3: sender_type in sendMessage API call
$content = $content -replace 'sender_type: ''dean''', 'sender_type: ''patient'''
Write-Host '✓ Restored sender_type in API call to patient' -ForegroundColor Green

# UNDO Change 4 & 5: sender in local message objects (both text and voice)
$content = $content -replace 'sender: ''dean''', 'sender: ''student'''
Write-Host '✓ Restored local message sender to student' -ForegroundColor Green

# UNDO Change 6: Update comment
$content = $content -replace '// Start a new consultation for dean/president', '// Start a new consultation for this student'
Write-Host '✓ Restored comment' -ForegroundColor Green

# UNDO Change 7: Update patient_name
$content = $content -replace 'patient_name: ''Dean/President''', 'patient_name: ''Current Student'''
Write-Host '✓ Restored patient_name' -ForegroundColor Green

# UNDO Change 8: Update complaint message
$content = $content -replace 'General consultation request - Dean/President seeking healthcare assistance', 'General consultation request - Student seeking healthcare assistance'
Write-Host '✓ Restored complaint message' -ForegroundColor Green

Write-Host "`nSaving changes..." -ForegroundColor Cyan
Set-Content $filePath -Value $content -NoNewline

Write-Host "`n✅ All changes have been UNDONE successfully!" -ForegroundColor Green
Write-Host "The file has been restored back to 'student' sender type" -ForegroundColor Yellow

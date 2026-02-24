# Add identifier_id display to user profile in sidebar

$filePath = 'c:\xampp\htdocs\iClini V.2\pages\deans_president\Deans_consultationchat.html'

Write-Host "Reading file..." -ForegroundColor Cyan
$content = Get-Content $filePath -Raw

Write-Host "Adding identifier_id display..." -ForegroundColor Yellow

# Replace the position line with both position and identifier_id
$oldLine = '<p class="text-xs text-green-300 text-left" style="font-size: 10px;">{{ user.position if user and user.position else ''Student'' }}</p>'

$newLines = @'
<p class="text-xs text-green-300 text-left" style="font-size: 10px;">{{ user.position if user and user.position else 'Dean/President' }}</p>
                            {% if user.identifier_id %}
                            <p class="text-xs text-yellow-300 font-mono text-left" style="font-size: 10px;">{{ user.identifier_id }}</p>
                            {% endif %}
'@

$content = $content -replace [regex]::Escape($oldLine), $newLines

Write-Host "`nSaving changes..." -ForegroundColor Cyan
Set-Content $filePath -Value $content -NoNewline

Write-Host "`n✅ Identifier ID display added!" -ForegroundColor Green
Write-Host "Will show DEAN-001 or PRES-001 below the position" -ForegroundColor Yellow

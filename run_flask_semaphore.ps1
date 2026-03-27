$ErrorActionPreference = 'Stop'

# Run Flask app with Semaphore SMS provider configuration

$apiKey = Read-Host -Prompt 'Enter SEMAPHORE_API_KEY'
$senderName = Read-Host -Prompt 'Enter SEMAPHORE_SENDER_NAME (optional, press Enter to skip)'

$env:SMS_PROVIDER = 'semaphore'
$env:SEMAPHORE_API_KEY = $apiKey

if ([string]::IsNullOrWhiteSpace($senderName)) {
    if (Test-Path Env:SEMAPHORE_SENDER_NAME) {
        Remove-Item Env:SEMAPHORE_SENDER_NAME
    }
} else {
    $env:SEMAPHORE_SENDER_NAME = $senderName
}

Write-Host 'Starting Flask with SMS_PROVIDER=semaphore ...'
python app.py

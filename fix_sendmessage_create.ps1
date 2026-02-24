# Fix sendMessage to create consultation if it doesn't exist

$filePath = 'c:\xampp\htdocs\iClini V.2\pages\deans_president\Deans_consultationchat.html'

Write-Host "Reading file..." -ForegroundColor Cyan
$content = Get-Content $filePath -Raw

Write-Host "Updating sendMessage function..." -ForegroundColor Yellow

# Replace the sendMessage function to create consultation if needed
$oldSendMessage = @'
    async sendMessage() {
        if (this.newMessage.trim() === '' || !this.currentConsultationId) return;
        
        const messageText = this.newMessage.trim();
        this.newMessage = '';
        
        try {
            const response = await fetch(`/api/online-consultations/${this.currentConsultationId}/send-message`, {
'@

$newSendMessage = @'
    async sendMessage() {
        if (this.newMessage.trim() === '') return;
        
        // Create consultation if it doesn't exist yet
        if (!this.currentConsultationId) {
            await this.initializeConsultation();
            if (!this.currentConsultationId) {
                alert('Failed to start consultation. Please try again.');
                return;
            }
        }
        
        const messageText = this.newMessage.trim();
        this.newMessage = '';
        
        try {
            const response = await fetch(`/api/online-consultations/${this.currentConsultationId}/send-message`, {
'@

$content = $content -replace [regex]::Escape($oldSendMessage), $newSendMessage

Write-Host "`nSaving changes..." -ForegroundColor Cyan
Set-Content $filePath -Value $content -NoNewline

Write-Host "`n✅ Fixed!" -ForegroundColor Green
Write-Host "sendMessage will now create consultation on first message" -ForegroundColor Yellow

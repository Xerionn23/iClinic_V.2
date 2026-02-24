import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html'

print("🔧 Updating isDateBlocked() and getBlockedReason() functions...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Update isDateBlocked function to check weekends first
    old_is_blocked = '''                isDateBlocked(dateStr) {
                    if (!dateStr) return false;
                    
                    // Check if date is in the past (using LOCAL timezone, not UTC)
                    const today = new Date();
                    const year = today.getFullYear();
                    const month = String(today.getMonth() + 1).padStart(2, '0');
                    const day = String(today.getDate()).padStart(2, '0');
                    const todayStr = `${year}-${month}-${day}`;
                    
                    if (dateStr < todayStr) {
                        return true; // Block booking on past dates
                    }'''
    
    new_is_blocked = '''                isDateBlocked(dateStr) {
                    if (!dateStr) return false;
                    
                    // Check if date is weekend (Saturday or Sunday)
                    const checkDate = new Date(dateStr + 'T12:00:00');
                    const dayOfWeek = checkDate.getDay();
                    if (dayOfWeek === 0 || dayOfWeek === 6) {
                        return true; // Block weekends - Clinic closed
                    }
                    
                    // Check if date is in the past (using LOCAL timezone, not UTC)
                    const today = new Date();
                    const year = today.getFullYear();
                    const month = String(today.getMonth() + 1).padStart(2, '0');
                    const day = String(today.getDate()).padStart(2, '0');
                    const todayStr = `${year}-${month}-${day}`;
                    
                    if (dateStr < todayStr) {
                        return true; // Block booking on past dates
                    }'''
    
    content = content.replace(old_is_blocked, new_is_blocked)
    
    # Update getBlockedReason function to include weekend message
    old_get_reason = '''                getBlockedReason(dateStr) {
                    if (!dateStr) return 'Unknown reason';
                    
                    const events = Array.isArray(this.clinicEvents) ? this.clinicEvents : [];'''
    
    new_get_reason = '''                getBlockedReason(dateStr) {
                    if (!dateStr) return 'Unknown reason';
                    
                    // Check if weekend first
                    const checkDate = new Date(dateStr + 'T12:00:00');
                    const dayOfWeek = checkDate.getDay();
                    if (dayOfWeek === 0) {
                        return 'Sunday - Clinic is closed on weekends';
                    }
                    if (dayOfWeek === 6) {
                        return 'Saturday - Clinic is closed on weekends';
                    }
                    
                    const events = Array.isArray(this.clinicEvents) ? this.clinicEvents : [];'''
    
    content = content.replace(old_get_reason, new_get_reason)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully updated functions!")
        print("\n📋 Changes made:")
        print("   - isDateBlocked() now checks for weekends")
        print("   - getBlockedReason() shows weekend message")
        print("   - Weekend dates will show as blocked in UI")
        print("\n🏥 Weekend Blocking:")
        print("   ❌ Saturday: 'Clinic is closed on weekends'")
        print("   ❌ Sunday: 'Clinic is closed on weekends'")
    else:
        print("⚠️  No changes made - pattern not found")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

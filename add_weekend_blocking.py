import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-appointment.html'

print("🔧 Adding weekend blocking to appointment system...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Find the section where we check for past dates and add weekend check before it
    old_code = '''                    // Mark availability considering clinic events
                    return timeSlots.map(slot => {
                        let available = !bookedTimes.has(slot.time);
                        
                        // PAST DATE BLOCKING: Block ALL time slots for past dates
                        if (isPastDate) {'''
    
    new_code = '''                    // Check if selected date is weekend (Saturday=6, Sunday=0)
                    const selectedDateObj = new Date(this.selectedDate + 'T12:00:00');
                    const dayOfWeek = selectedDateObj.getDay();
                    const isWeekend = (dayOfWeek === 0 || dayOfWeek === 6); // Sunday=0, Saturday=6
                    
                    if (isWeekend) {
                        console.log(`🚫 WEEKEND BLOCK: ${this.selectedDate} is ${dayOfWeek === 0 ? 'Sunday' : 'Saturday'} - Clinic is closed`);
                    }
                    
                    // Mark availability considering clinic events
                    return timeSlots.map(slot => {
                        let available = !bookedTimes.has(slot.time);
                        
                        // WEEKEND BLOCKING: Block ALL time slots for Saturday and Sunday
                        if (isWeekend) {
                            available = false;
                            console.log(`🚫 Weekend block: ${slot.time} on ${this.selectedDate} (Clinic closed on weekends)`);
                        }
                        // PAST DATE BLOCKING: Block ALL time slots for past dates
                        else if (isPastDate) {'''
    
    content = content.replace(old_code, new_code)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully added weekend blocking!")
        print("\n📋 Changes made:")
        print("   - Added weekend detection (Saturday & Sunday)")
        print("   - Block ALL time slots on weekends")
        print("   - Added console logging for debugging")
        print("\n🏥 Clinic Schedule:")
        print("   ✅ Monday - Friday: Open")
        print("   ❌ Saturday: CLOSED")
        print("   ❌ Sunday: CLOSED")
    else:
        print("⚠️  Pattern not found - checking alternative location...")
        
        # Try alternative pattern
        old_code2 = '''                    return timeSlots.map(slot => {
                        let available = !bookedTimes.has(slot.time);
                        
                        // PAST DATE BLOCKING: Block ALL time slots for past dates
                        if (isPastDate) {'''
        
        new_code2 = '''                    // Check if selected date is weekend (Saturday=6, Sunday=0)
                    const selectedDateObj = new Date(this.selectedDate + 'T12:00:00');
                    const dayOfWeek = selectedDateObj.getDay();
                    const isWeekend = (dayOfWeek === 0 || dayOfWeek === 6);
                    
                    if (isWeekend) {
                        console.log(`🚫 WEEKEND: ${this.selectedDate} is ${dayOfWeek === 0 ? 'Sunday' : 'Saturday'} - Clinic closed`);
                    }
                    
                    return timeSlots.map(slot => {
                        let available = !bookedTimes.has(slot.time);
                        
                        // WEEKEND BLOCKING: Clinic closed on Saturday and Sunday
                        if (isWeekend) {
                            available = false;
                        }
                        // PAST DATE BLOCKING: Block ALL time slots for past dates
                        else if (isPastDate) {'''
        
        content = original_content.replace(old_code2, new_code2)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Applied alternative fix - weekend blocking added!")
        else:
            print("❌ Could not find pattern to update")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

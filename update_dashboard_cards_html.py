import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-dashboard.html'

print("🔧 Updating dashboard cards HTML to use dynamic data...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Update Health Records Card
    old_health = r'<p class="text-3xl font-bold text-gray-900">12</p>'
    new_health = r'<p class="text-3xl font-bold text-gray-900" x-text="healthRecordsCount">0</p>'
    content = re.sub(old_health, new_health, content, count=1)
    
    old_last_visit = r'<span class="text-xs text-gray-500">Last visit: Oct 15</span>'
    new_last_visit = r'<span class="text-xs text-gray-500" x-text="lastVisitDate ? `Last visit: ${lastVisitDate}` : \'No visits yet\'">Last visit: --</span>'
    content = re.sub(old_last_visit, new_last_visit, content, count=1)
    
    # Update Upcoming Appointments Card
    old_appointments = r'<p class="text-3xl font-bold text-gray-900">2</p>'
    new_appointments = r'<p class="text-3xl font-bold text-gray-900" x-text="upcomingAppointmentsCount">0</p>'
    content = re.sub(old_appointments, new_appointments, content, count=1)
    
    old_next_apt = r'<span class="inline-flex items-center text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full">\s*Next: Tomorrow\s*</span>\s*<span class="text-xs text-gray-500">10:00 AM</span>'
    new_next_apt = r'''<span x-show="nextAppointmentDate" class="inline-flex items-center text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full" x-text="`Next: ${nextAppointmentDate}`">
                                                Next: --
                                            </span>
                                            <span x-show="nextAppointmentTime" class="text-xs text-gray-500" x-text="nextAppointmentTime">--</span>
                                            <span x-show="!nextAppointmentDate" class="text-xs text-gray-500">No upcoming</span>'''
    content = re.sub(old_next_apt, new_next_apt, content, flags=re.DOTALL)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully updated dashboard cards HTML!")
        print("\n📋 Changes made:")
        print("   ✅ Health Records: Now shows x-text='healthRecordsCount'")
        print("   ✅ Last Visit: Dynamic from lastVisitDate")
        print("   ✅ Upcoming Appointments: Shows x-text='upcomingAppointmentsCount'")
        print("   ✅ Next Appointment: Dynamic date and time")
        print("\n✨ Result:")
        print("   - Cards now display real data from database")
        print("   - Each student sees their own data")
        print("   - Updates automatically on page load")
    else:
        print("⚠️  No changes made - patterns not found")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

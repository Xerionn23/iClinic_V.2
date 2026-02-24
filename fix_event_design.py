import re

# Read the file
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Appointments.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the event icon design
old_pattern = r'''<!-- Clinic Events for Selected Date -->
                                    <template x-for="event in filteredClinicEvents" :key="event\.id">
                                        <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                                            <div class="flex items-center gap-4">
                                                <div class="w-12 h-12 rounded-full flex items-center justify-center"
                                                     :class="\{
                                                         'bg-gradient-to-br from-red-300 to-red-400': event\.event_type === 'no_appointments',
                                                         'bg-gradient-to-br from-yellow-300 to-yellow-400': event\.event_type === 'limited_hours',
                                                         'bg-gradient-to-br from-purple-300 to-purple-400': event\.event_type === 'emergency_only',
                                                         'bg-gradient-to-br from-blue-300 to-blue-400': event\.event_type === 'maintenance',
                                                         'bg-gradient-to-br from-green-300 to-green-400': event\.event_type === 'holiday'
                                                     \}">
                                                    <i :data-feather="event\.event_type === 'no_appointments' \? 'x-circle' : 
                                                                      event\.event_type === 'limited_hours' \? 'clock' :
                                                                      event\.event_type === 'emergency_only' \? 'alert-triangle' :
                                                                      event\.event_type === 'maintenance' \? 'tool' :
                                                                      'calendar'" 
                                                       class="w-6 h-6 text-white"></i>
                                                </div>'''

new_pattern = '''<!-- Clinic Events for Selected Date -->
                                    <template x-for="event in filteredClinicEvents" :key="event.id">
                                        <div class="flex items-center justify-between p-4 rounded-lg transition-all duration-200 hover:shadow-lg"
                                             :class="{
                                                 'bg-red-50 border-2 border-red-200': event.event_type === 'no_appointments',
                                                 'bg-yellow-50 border-2 border-yellow-200': event.event_type === 'limited_hours',
                                                 'bg-purple-50 border-2 border-purple-200': event.event_type === 'emergency_only',
                                                 'bg-blue-50 border-2 border-blue-200': event.event_type === 'maintenance',
                                                 'bg-green-50 border-2 border-green-200': event.event_type === 'holiday'
                                             }">
                                            <div class="flex items-center gap-4">
                                                <div class="relative">
                                                    <div class="w-14 h-14 rounded-xl flex items-center justify-center shadow-lg transform transition-transform hover:scale-110"
                                                         :class="{
                                                             'bg-gradient-to-br from-red-500 to-red-600': event.event_type === 'no_appointments',
                                                             'bg-gradient-to-br from-yellow-500 to-yellow-600': event.event_type === 'limited_hours',
                                                             'bg-gradient-to-br from-purple-500 to-purple-600': event.event_type === 'emergency_only',
                                                             'bg-gradient-to-br from-blue-500 to-blue-600': event.event_type === 'maintenance',
                                                             'bg-gradient-to-br from-green-500 to-green-600': event.event_type === 'holiday'
                                                         }">
                                                        <i :data-feather="event.event_type === 'no_appointments' ? 'x-circle' : 
                                                                          event.event_type === 'limited_hours' ? 'clock' :
                                                                          event.event_type === 'emergency_only' ? 'alert-triangle' :
                                                                          event.event_type === 'maintenance' ? 'tool' :
                                                                          'calendar'" 
                                                           class="w-7 h-7 text-white"></i>
                                                    </div>
                                                    <!-- Pulse animation for important events -->
                                                    <div x-show="event.event_type === 'no_appointments' || event.event_type === 'emergency_only'" 
                                                         class="absolute -top-1 -right-1 w-3 h-3 rounded-full animate-pulse"
                                                         :class="{
                                                             'bg-red-500': event.event_type === 'no_appointments',
                                                             'bg-purple-500': event.event_type === 'emergency_only'
                                                         }"></div>
                                                </div>'''

# Replace using regex
content = re.sub(old_pattern, new_pattern, content, flags=re.DOTALL)

# Write back
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Appointments.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Event design updated successfully!")

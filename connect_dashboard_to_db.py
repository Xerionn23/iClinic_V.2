import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-dashboard.html'

print("🔧 Connecting dashboard cards to database...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Step 1: Add new data properties for real data
    old_data = '''    patientCount: 1234,
    appointmentCount: 28,
    revenue: 85420,
    staffCount: 12,
    chartInstance: null,
    announcements: [],
    clinicStatus: 'Checking...',
    clinicStatusColor: 'gray',
    recentActivities: [],'''
    
    new_data = '''    // Dashboard Stats - Real Data
    healthRecordsCount: 0,
    upcomingAppointmentsCount: 0,
    nextAppointmentDate: null,
    nextAppointmentTime: null,
    lastVisitDate: null,
    announcements: [],
    clinicStatus: 'Checking...',
    clinicStatusColor: 'gray',
    loading: true,'''
    
    content = content.replace(old_data, new_data)
    
    # Step 2: Add data loading functions after init()
    init_end_pattern = r"(this\.checkClinicStatus\(\);[\s\S]*?\}\);[\s\S]*?this\.loadAnnouncements\(\);)"
    
    new_functions = r'''\1
        
        // Load real dashboard data
        this.loadDashboardData();'''
    
    content = re.sub(init_end_pattern, new_functions, content, count=1)
    
    # Step 3: Add the loadDashboardData function before the closing }
    functions_to_add = '''
    
    async loadDashboardData() {
        try {
            this.loading = true;
            
            // Load health records count
            const healthResponse = await fetch('/api/student/health-records', {
                credentials: 'same-origin'
            });
            if (healthResponse.ok) {
                const healthData = await healthResponse.json();
                this.healthRecordsCount = healthData.length || 0;
                
                // Get last visit date from most recent record
                if (healthData.length > 0) {
                    const sortedRecords = healthData.sort((a, b) => 
                        new Date(b.visit_date) - new Date(a.visit_date)
                    );
                    const lastVisit = new Date(sortedRecords[0].visit_date);
                    this.lastVisitDate = lastVisit.toLocaleDateString('en-US', { 
                        month: 'short', 
                        day: 'numeric' 
                    });
                }
            }
            
            // Load appointments
            const appointmentsResponse = await fetch('/api/student/appointments', {
                credentials: 'same-origin'
            });
            if (appointmentsResponse.ok) {
                const appointments = await appointmentsResponse.json();
                
                // Filter upcoming appointments (confirmed status, future dates)
                const now = new Date();
                const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
                
                const upcoming = appointments.filter(apt => {
                    if (apt.status !== 'confirmed' && apt.status !== 'Confirmed') return false;
                    const aptDate = new Date(apt.date);
                    return aptDate >= today;
                }).sort((a, b) => new Date(a.date) - new Date(b.date));
                
                this.upcomingAppointmentsCount = upcoming.length;
                
                // Get next appointment details
                if (upcoming.length > 0) {
                    const nextApt = upcoming[0];
                    const aptDate = new Date(nextApt.date);
                    const tomorrow = new Date(today);
                    tomorrow.setDate(tomorrow.getDate() + 1);
                    
                    if (aptDate.toDateString() === today.toDateString()) {
                        this.nextAppointmentDate = 'Today';
                    } else if (aptDate.toDateString() === tomorrow.toDateString()) {
                        this.nextAppointmentDate = 'Tomorrow';
                    } else {
                        this.nextAppointmentDate = aptDate.toLocaleDateString('en-US', { 
                            month: 'short', 
                            day: 'numeric' 
                        });
                    }
                    
                    this.nextAppointmentTime = nextApt.time || '10:00 AM';
                }
            }
            
            this.loading = false;
            console.log('✅ Dashboard data loaded:', {
                healthRecords: this.healthRecordsCount,
                upcomingAppointments: this.upcomingAppointmentsCount,
                nextAppointment: this.nextAppointmentDate,
                lastVisit: this.lastVisitDate
            });
            
        } catch (error) {
            console.error('❌ Error loading dashboard data:', error);
            this.loading = false;
        }
    },'''
    
    # Find the last function before the closing brace
    pattern = r"(checkClinicStatus\(\) \{[\s\S]*?\},)\s*(\n\s*animateNumbers)"
    replacement = r"\1" + functions_to_add + r"\2"
    content = re.sub(pattern, replacement, content, count=1)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully connected dashboard to database!")
        print("\n📋 Changes made:")
        print("   - Added real data properties (healthRecordsCount, upcomingAppointmentsCount, etc.)")
        print("   - Added loadDashboardData() function")
        print("   - Fetches data from /api/student/health-records")
        print("   - Fetches data from /api/student/appointments")
        print("   - Calculates upcoming appointments and last visit")
        print("\n✅ Next step: Update HTML to use dynamic data")
    else:
        print("⚠️  No changes made - pattern not found")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

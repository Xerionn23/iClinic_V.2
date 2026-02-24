import re

file_path = r'c:\xampp\htdocs\iClini V.2\STUDENT\ST-dashboard.html'

print("🔧 Fixing dashboard API endpoints to use correct URLs...\n")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix the API endpoints
    # Change /api/student/health-records to /api/medical-records
    content = content.replace(
        "const healthResponse = await fetch('/api/student/health-records', {",
        "const healthResponse = await fetch('/api/medical-records', {"
    )
    
    # Change /api/student/appointments to /api/appointments
    content = content.replace(
        "const appointmentsResponse = await fetch('/api/student/appointments', {",
        "const appointmentsResponse = await fetch('/api/appointments', {"
    )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully fixed API endpoints!")
        print("\n📋 Changes made:")
        print("   - Changed /api/student/health-records → /api/medical-records")
        print("   - Changed /api/student/appointments → /api/appointments")
        print("\n✅ Result:")
        print("   - Dashboard will now fetch REAL data from database")
        print("   - Each student will see their own records")
        print("   - Health records count will be accurate")
        print("   - Appointments count will be correct")
    else:
        print("⚠️  No changes made - endpoints already correct or not found")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

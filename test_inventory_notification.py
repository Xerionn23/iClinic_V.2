"""
Test script for inventory notification system
Run this to test if the notification system is working
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("🧪 Testing iClinic Inventory Notification System")
print("=" * 70)

# Test 1: Import modules
print("\n1️⃣ Testing imports...")
try:
    from services.inventory_notification_service import (
        get_inventory_alerts,
        get_nurse_emails,
        send_inventory_notification_email
    )
    print("   ✅ All modules imported successfully")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    exit(1)

# Test 2: Database connection
print("\n2️⃣ Testing database connection...")
try:
    from config.database import DatabaseConfig
    conn = DatabaseConfig.get_connection()
    if conn:
        print("   ✅ Database connection successful")
        conn.close()
    else:
        print("   ❌ Database connection failed")
        exit(1)
except Exception as e:
    print(f"   ❌ Database connection error: {e}")
    exit(1)

# Test 3: Get inventory alerts
print("\n3️⃣ Checking inventory alerts...")
try:
    alerts = get_inventory_alerts()
    if alerts:
        total = (
            len(alerts['expiring_30_days']) + 
            len(alerts['low_stock'])
        )
        print(f"   ✅ Inventory check successful")
        print(f"   📊 Total alerts: {total}")
        print(f"      ⚠️  Expiring in 30 days: {len(alerts['expiring_30_days'])}")
        print(f"       Low stock: {len(alerts['low_stock'])}")
        
        if total == 0:
            print("\n   ℹ️  No alerts found - inventory is healthy!")
            print("   💡 To test email, you can manually add test data to medicine_batches")
    else:
        print("   ❌ Failed to get inventory alerts")
        exit(1)
except Exception as e:
    print(f"   ❌ Error checking alerts: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Get nurse emails
print("\n4️⃣ Checking nurse emails...")
try:
    nurse_emails = get_nurse_emails()
    if nurse_emails:
        print(f"   ✅ Found {len(nurse_emails)} nurse email(s)")
        for email in nurse_emails:
            print(f"      📧 {email}")
    else:
        print("   ⚠️  No nurse emails found in database")
        print("   💡 Using system email as fallback: norzagaraycollege.clinic@gmail.com")
        nurse_emails = ['norzagaraycollege.clinic@gmail.com']
except Exception as e:
    print(f"   ❌ Error getting nurse emails: {e}")
    exit(1)

# Test 5: Ask user if they want to send test email
print("\n5️⃣ Email notification test")
print("   ⚠️  This will send an actual email to the nurse(s)")

# Check if there are alerts to send
alerts = get_inventory_alerts()
total_alerts = (
    len(alerts['expiring_30_days']) + 
    len(alerts['low_stock'])
)

if total_alerts == 0:
    print("\n   ℹ️  No alerts to send - skipping email test")
    print("   💡 All tests passed! System is ready.")
else:
    env_choice = (os.environ.get('ICLINIC_SEND_TEST_EMAIL') or '').strip().lower()
    if env_choice in ['1', 'true', 'yes', 'y', 'on']:
        response = 'yes'
    elif env_choice in ['0', 'false', 'no', 'n', 'off']:
        response = 'no'
    elif not sys.stdin.isatty():
        # Non-interactive run (e.g. IDE tooling). Default to sending.
        response = 'yes'
    else:
        try:
            response = input("\n   Do you want to send test email? (yes/no): ").strip().lower()
        except EOFError:
            response = 'yes'
    
    if response in ['yes', 'y']:
        print("\n   📧 Sending test email...")
        try:
            success = send_inventory_notification_email(nurse_emails)
            if success:
                print("   ✅ Test email sent successfully!")
                print(f"   📬 Check inbox: {', '.join(nurse_emails)}")
            else:
                print("   ❌ Failed to send test email")
                exit(1)
        except Exception as e:
            print(f"   ❌ Error sending email: {e}")
            import traceback
            traceback.print_exc()
            exit(1)
    else:
        print("   ⏭️  Skipping email test")

# Summary
print("\n" + "=" * 70)
print("✅ All tests completed successfully!")
print("=" * 70)
print("\n📋 Next Steps:")
print("   1. Run SETUP_DAILY_INVENTORY_NOTIFICATIONS.bat to schedule daily emails")
print("   2. Or use: python run_daily_inventory_check.py to test scheduled task")
print("   3. Check INVENTORY_NOTIFICATION_GUIDE.md for full documentation")
print("\n" + "=" * 70)

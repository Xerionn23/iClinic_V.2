"""
Daily Inventory Check Script
Run this script daily to check inventory and send email notifications to nurses
Can be scheduled using Windows Task Scheduler or cron job
"""

import requests
import sys
from datetime import datetime

# Configuration
API_URL = "http://127.0.0.1:5000/api/inventory/schedule-notification"

def run_inventory_check():
    """Run the daily inventory check and send notifications"""
    print("=" * 70)
    print(f"🏥 iClinic Daily Inventory Check")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    try:
        # Make POST request to the scheduled notification endpoint
        print("\n📡 Connecting to iClinic server...")
        response = requests.post(API_URL, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print(f"\n✅ {data.get('message')}")
                
                if data.get('total_alerts', 0) > 0:
                    print(f"\n📊 Alert Summary:")
                    print(f"   Total Alerts: {data.get('total_alerts')}")
                    print(f"   Recipients: {', '.join(data.get('recipients', []))}")
                    print(f"\n📧 Email notification sent successfully!")
                else:
                    print(f"\n✅ No inventory alerts found - system is healthy!")
                
                return True
            else:
                print(f"\n⚠️ Warning: {data.get('message', 'Unknown response')}")
                return True
        else:
            print(f"\n❌ Error: Server returned status code {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to iClinic server")
        print("   Please ensure the Flask server is running on http://127.0.0.1:5000")
        return False
    except requests.exceptions.Timeout:
        print("\n❌ Error: Request timed out")
        print("   The server took too long to respond")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_inventory_check()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ Daily inventory check completed successfully!")
    else:
        print("❌ Daily inventory check failed!")
    print("=" * 70)
    
    # Exit with appropriate code for task scheduler
    sys.exit(0 if success else 1)

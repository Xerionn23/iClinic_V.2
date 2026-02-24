from config.database import DatabaseConfig
from datetime import datetime, timedelta

conn = DatabaseConfig.get_connection()
cursor = conn.cursor()

cursor.execute('SELECT medicine_name, expiry_date FROM medicines ORDER BY expiry_date')
medicines = cursor.fetchall()

today = datetime.now().date()
thirty_days = today + timedelta(days=30)

print(f'Today: {today}')
print(f'30 days from now: {thirty_days}')
print('\nMedicines Status:')

active = 0
expiring = 0

for m in medicines:
    name, expiry = m[0], m[1]
    if expiry:
        if isinstance(expiry, datetime):
            expiry_date = expiry.date()
        else:
            expiry_date = datetime.strptime(str(expiry), '%Y-%m-%d').date()
        
        if expiry_date <= today:
            print(f'  ❌ EXPIRED: {name} (expired {expiry_date})')
            expiring += 1
        elif expiry_date <= thirty_days:
            print(f'  ⚠️ EXPIRING SOON: {name} (expires {expiry_date})')
            expiring += 1
        else:
            print(f'  ✅ ACTIVE: {name} (expires {expiry_date})')
            active += 1
    else:
        print(f'  ✅ ACTIVE: {name} (no expiry)')
        active += 1

print(f'\n📊 Summary: {active} active, {expiring} expired/expiring')
print(f'Dashboard will show: {active} medicines')

cursor.close()
conn.close()

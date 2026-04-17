"""
Appointment Reminder Scheduler for iClinic
Scheduled task to send 3-day reminders to patients
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from services.patient_notification_service import send_three_day_reminder, get_patient_email
from config.database import DatabaseConfig

def check_and_send_reminders():
    """Check all appointments and send 3-day reminders to patients"""
    conn = DatabaseConfig.get_connection()
    if not conn:
        print("Database connection failed")
        return False
    
    cursor = conn.cursor(dictionary=True)
    today = datetime.now().date()
    reminder_date = today + timedelta(days=3)
    
    try:
        # Get appointments that are exactly 3 days from now and not cancelled
        cursor.execute('''
            SELECT id, patient, date, time, type, status, reminder_sent
            FROM appointments 
            WHERE date = %s 
            AND status NOT IN ('cancelled', 'canceled')
            AND (reminder_sent IS NULL OR reminder_sent = 0)
        ''', (reminder_date,))
        
        appointments_to_remind = cursor.fetchall()
        
        if not appointments_to_remind:
            print(f"No appointments found for {reminder_date} requiring reminders")
            return True
        
        print(f"Found {len(appointments_to_remind)} appointment(s) for {reminder_date} - sending reminders")
        
        reminders_sent = 0
        for appointment in appointments_to_remind:
            print(f"Sending reminder for appointment ID {appointment['id']} - {appointment['patient']}")
            
            # Get patient email
            patient_email = get_patient_email(appointment['patient'])
            
            if patient_email:
                # Send reminder
                reminder_sent = send_three_day_reminder(
                    patient_email=patient_email,
                    patient_name=appointment['patient'],
                    appointment_date=appointment['date'].strftime('%Y-%m-%d'),
                    appointment_time=str(appointment['time']),
                    appointment_type=appointment['type'],
                    appointment_id=appointment['id']
                )
                
                if reminder_sent:
                    # Mark reminder as sent
                    cursor.execute('''
                        UPDATE appointments 
                        SET reminder_sent = 1 
                        WHERE id = %s
                    ''', (appointment['id'],))
                    conn.commit()
                    reminders_sent += 1
                    print(f"Reminder sent to {patient_email}")
                else:
                    print(f"Failed to send reminder to {patient_email}")
            else:
                print(f"No email found for patient: {appointment['patient']}")
        
        print(f"Reminders sent: {reminders_sent}/{len(appointments_to_remind)}")
        return reminders_sent > 0
        
    except Exception as e:
        print(f"Error checking reminders: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Run the reminder check
    print("Running Appointment Reminder Scheduler...")
    print("=" * 60)
    
    success = check_and_send_reminders()
    
    if success:
        print("\nReminder check completed successfully!")
    else:
        print("\nReminder check failed!")

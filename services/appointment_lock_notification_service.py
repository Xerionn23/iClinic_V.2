"""
Appointment Lock Notification Service for iClinic
Sends email alerts to clinic nurses when appointments become non-cancellable/non-reschedulable (within 3 days)
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from config.database import DatabaseConfig

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'norzagaraycollege.clinic@gmail.com',
    'password': 'xtsweijcxsntwhld',
    'from_name': 'iClinic Management System'
}

def get_nurse_emails():
    """Get all clinic nurse email addresses from database"""
    conn = DatabaseConfig.get_connection()
    if not conn:
        print("Database connection failed")
        return ['norzagaraycollege.clinic@gmail.com']  # Fallback to system email
    
    cursor = conn.cursor()
    nurse_emails = []
    
    try:
        # Get emails from nurses table
        cursor.execute('SELECT email FROM nurses WHERE status = "Active" AND email IS NOT NULL AND email != ""')
        nurse_records = cursor.fetchall()
        
        for record in nurse_records:
            email = record[0].strip()
            if email and '@' in email:
                nurse_emails.append(email)
        
        # Also get staff users with nurse role
        cursor.execute('SELECT email FROM users WHERE role = "staff" AND email IS NOT NULL AND email != ""')
        staff_records = cursor.fetchall()
        
        for record in staff_records:
            email = record[0].strip()
            if email and '@' in email and email not in nurse_emails:
                nurse_emails.append(email)
        
        print(f"Found {len(nurse_emails)} nurse email(s)")
        
    except Exception as e:
        print(f"Error fetching nurse emails: {e}")
        nurse_emails = ['norzagaraycollege.clinic@gmail.com']
    finally:
        cursor.close()
        conn.close()
    
    return nurse_emails

def send_appointment_lock_notification(appointment_data):
    """Send email notification about appointment becoming non-cancellable"""
    try:
        nurse_emails = get_nurse_emails()
        
        if not nurse_emails:
            print("No nurse emails found")
            return False
        
        # Format appointment date and time
        appointment_date = appointment_data.get('date', '')
        appointment_time = appointment_data.get('time', '')
        patient_name = appointment_data.get('patient_name', '')
        appointment_type = appointment_data.get('type', '')
        
        # Format date for display
        try:
            date_obj = datetime.strptime(appointment_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
        except:
            formatted_date = appointment_date
        
        # Format time to 12-hour format
        try:
            time_obj = datetime.strptime(appointment_time, '%H:%M')
            formatted_time = time_obj.strftime('%I:%M %p')
        except:
            formatted_time = appointment_time
        
        # Create email content
        subject = f"🔒 APPOINTMENT LOCKED: {patient_name} - {formatted_date}"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointment Lock Notification</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: Arial, sans-serif;">
    <div style="max-width: 600px; margin: 20px auto; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0;">
            <div style="display: flex; align-items: center;">
                <div style="background-color: white; color: #dc2626; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                    <span style="font-size: 20px;">🔒</span>
                </div>
                <div>
                    <h1 style="margin: 0; font-size: 24px; font-weight: bold;">APPOINTMENT LOCKED</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Non-Cancellable & Non-Reschedulable</p>
                </div>
            </div>
        </div>
        
        <!-- Content -->
        <div style="padding: 30px;">
            <div style="background-color: #fef2f2; border-left: 4px solid #dc2626; padding: 15px; margin-bottom: 25px;">
                <p style="margin: 0; color: #991b1b; font-weight: 500;">
                    ⚠️ This appointment is now within 3 days and cannot be cancelled or rescheduled according to clinic policy.
                </p>
            </div>
            
            <h2 style="color: #1f2937; margin-bottom: 20px;">Appointment Details</h2>
            
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 25px;">
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: 600; color: #6b7280; width: 140px;">Patient Name:</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #1f2937;">{patient_name}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: 600; color: #6b7280;">Date:</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #1f2937;">{formatted_date}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: 600; color: #6b7280;">Time:</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #1f2937;">{formatted_time}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: 600; color: #6b7280;">Type:</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #1f2937;">{appointment_type}</td>
                </tr>
            </table>
            
            <div style="background-color: #f9fafb; padding: 20px; border-radius: 6px; margin-bottom: 25px;">
                <h3 style="color: #1f2937; margin-top: 0; margin-bottom: 10px;">📋 Important Notes:</h3>
                <ul style="margin: 0; padding-left: 20px; color: #4b5563;">
                    <li style="margin-bottom: 8px;">This appointment is within the 3-day lock period</li>
                    <li style="margin-bottom: 8px;">Cancellation and rescheduling are no longer permitted</li>
                    <li style="margin-bottom: 8px;">Please ensure patient attends the scheduled appointment</li>
                    <li style="margin-bottom: 0;">Prepare necessary resources for this consultation</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <p style="color: #6b7280; font-size: 14px; margin: 0;">
                    This is an automated notification from the iClinic Management System.<br>
                    Please do not reply to this email.
                </p>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-radius: 0 0 8px 8px; border-top: 1px solid #e5e7eb;">
            <p style="margin: 0; color: #6b7280; font-size: 12px;">
                iClinic Management System • Norzagaray College<br>
                Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </p>
        </div>
    </div>
</body>
</html>
        """
        
        # Send email to all nurses
        cfg = EMAIL_CONFIG
        success_count = 0
        
        for nurse_email in nurse_emails:
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = f"{cfg['from_name']} <{cfg['email']}>"
                msg['To'] = nurse_email
                msg.attach(MIMEText(html_content, 'html'))
                
                # Connect to SMTP server
                server = smtplib.SMTP(cfg['smtp_server'], cfg['smtp_port'])
                server.starttls()
                server.login(cfg['email'], cfg['password'])
                server.send_message(msg)
                server.quit()
                
                success_count += 1
                print(f"Appointment lock notification sent to: {nurse_email}")
                
            except Exception as e:
                print(f"Failed to send to {nurse_email}: {e}")
        
        print(f"Appointment lock notifications sent: {success_count}/{len(nurse_emails)}")
        return success_count > 0
        
    except Exception as e:
        print(f"Error sending appointment lock notification: {e}")
        return False

def check_and_send_lock_notifications():
    """Check all appointments and send notifications for those within 3 days"""
    conn = DatabaseConfig.get_connection()
    if not conn:
        print("Database connection failed")
        return False
    
    cursor = conn.cursor(dictionary=True)
    today = datetime.now().date()
    lock_threshold = today + timedelta(days=3)
    
    try:
        # Get appointments that are within 3 days and not cancelled
        cursor.execute('''
            SELECT id, patient_name, date, time, type, status, lock_notification_sent
            FROM appointments 
            WHERE date <= %s 
            AND date >= %s 
            AND status NOT IN ('cancelled', 'canceled')
            AND (lock_notification_sent IS NULL OR lock_notification_sent = 0)
        ''', (lock_threshold, today))
        
        appointments_to_notify = cursor.fetchall()
        
        if not appointments_to_notify:
            print("No appointments within lock period requiring notification")
            return True
        
        print(f"Found {len(appointments_to_notify)} appointment(s) within lock period")
        
        notifications_sent = 0
        for appointment in appointments_to_notify:
            print(f"Sending lock notification for appointment ID {appointment['id']}")
            
            if send_appointment_lock_notification(appointment):
                # Mark notification as sent
                cursor.execute('''
                    UPDATE appointments 
                    SET lock_notification_sent = 1 
                    WHERE id = %s
                ''', (appointment['id'],))
                conn.commit()
                notifications_sent += 1
            else:
                print(f"Failed to send notification for appointment ID {appointment['id']}")
        
        print(f"Lock notifications sent: {notifications_sent}/{len(appointments_to_notify)}")
        return notifications_sent > 0
        
    except Exception as e:
        print(f"Error checking lock notifications: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Test the notification system
    print("Testing Appointment Lock Notification System...")
    print("=" * 60)
    
    # Test with sample appointment data
    test_appointment = {
        'patient_name': 'Juan Dela Cruz',
        'date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
        'time': '10:30',
        'type': 'General Consultation'
    }
    
    print(f"Sending test notification for: {test_appointment['patient_name']}")
    success = send_appointment_lock_notification(test_appointment)
    
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")

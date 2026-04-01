"""
Patient Notification Service for iClinic
Sends email notifications to patients:
1. Booking confirmation (immediate)
2. 3-day reminder before appointment
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

def send_booking_confirmation(patient_email, patient_name, appointment_date, appointment_time, appointment_type):
    """Send booking confirmation email to patient"""
    try:
        # Format appointment date and time
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
        subject = f"✅ Appointment Confirmed: {formatted_date} at {formatted_time}"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointment Confirmation</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: Arial, sans-serif;">
    <div style="max-width: 600px; margin: 20px auto; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0;">
            <div style="display: flex; align-items: center;">
                <div style="background-color: white; color: #10b981; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                    <span style="font-size: 20px;">✓</span>
                </div>
                <div>
                    <h1 style="margin: 0; font-size: 24px; font-weight: bold;">APPOINTMENT CONFIRMED</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Your appointment has been successfully booked</p>
                </div>
            </div>
        </div>
        
        <!-- Content -->
        <div style="padding: 30px;">
            <div style="background-color: #f0fdf4; border-left: 4px solid #10b981; padding: 15px; margin-bottom: 25px;">
                <p style="margin: 0; color: #166534; font-weight: 500;">
                    ✅ Your appointment has been confirmed and scheduled. Please save this information for your reference.
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
            
            <div style="background-color: #fef3c7; padding: 20px; border-radius: 6px; margin-bottom: 25px;">
                <h3 style="color: #92400e; margin-top: 0; margin-bottom: 10px;">📅 Important Reminder:</h3>
                <ul style="margin: 0; padding-left: 20px; color: #78350f;">
                    <li style="margin-bottom: 8px;">Please arrive 10 minutes before your scheduled time</li>
                    <li style="margin-bottom: 8px;">Bring your valid ID for verification</li>
                    <li style="margin-bottom: 8px;">Cancellation or rescheduling is not allowed within 3 days of the appointment</li>
                    <li style="margin-bottom: 0;">You will receive a reminder email 3 days before your appointment</li>
                </ul>
            </div>
            
            <div style="background-color: #f9fafb; padding: 20px; border-radius: 6px; margin-bottom: 25px;">
                <h3 style="color: #1f2937; margin-top: 0; margin-bottom: 10px;">📍 Clinic Information:</h3>
                <p style="margin: 0; color: #4b5563; line-height: 1.6;">
                    <strong>Norzagaray College Clinic</strong><br>
                    Norzagaray, Bulacan<br>
                    Please bring this confirmation email on your appointment day.
                </p>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <p style="color: #6b7280; font-size: 14px; margin: 0;">
                    This is an automated notification from the iClinic Management System.<br>
                    Please do not reply to this email. For inquiries, visit the clinic directly.
                </p>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-radius: 0 0 8px 8px; border-top: 1px solid #e5e7eb;">
            <p style="margin: 0; color: #6b7280; font-size: 12px;">
                iClinic Management System • Norzagaray College<br>
                Confirmation sent on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </p>
        </div>
    </div>
</body>
</html>
        """
        
        # Send email
        cfg = EMAIL_CONFIG
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{cfg['from_name']} <{cfg['email']}>"
        msg['To'] = patient_email
        msg.attach(MIMEText(html_content, 'html'))
        
        # Connect to SMTP server
        server = smtplib.SMTP(cfg['smtp_server'], cfg['smtp_port'])
        server.starttls()
        server.login(cfg['email'], cfg['password'])
        server.send_message(msg)
        server.quit()
        
        print(f"Booking confirmation sent to: {patient_email}")
        return True
        
    except Exception as e:
        print(f"Error sending booking confirmation: {e}")
        return False

def send_three_day_reminder(patient_email, patient_name, appointment_date, appointment_time, appointment_type):
    """Send 3-day reminder email to patient"""
    try:
        # Format appointment date and time
        try:
            date_obj = datetime.strptime(appointment_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
            days_until = (date_obj - datetime.now().date()).days
        except:
            formatted_date = appointment_date
            days_until = 3
        
        # Format time to 12-hour format
        try:
            time_obj = datetime.strptime(appointment_time, '%H:%M')
            formatted_time = time_obj.strftime('%I:%M %p')
        except:
            formatted_time = appointment_time
        
        # Create email content
        subject = f"⏰ Reminder: Your appointment is in {days_until} days!"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointment Reminder</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: Arial, sans-serif;">
    <div style="max-width: 600px; margin: 20px auto; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0;">
            <div style="display: flex; align-items: center;">
                <div style="background-color: white; color: #f59e0b; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                    <span style="font-size: 20px;">⏰</span>
                </div>
                <div>
                    <h1 style="margin: 0; font-size: 24px; font-weight: bold;">APPOINTMENT REMINDER</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Your appointment is coming up soon!</p>
                </div>
            </div>
        </div>
        
        <!-- Content -->
        <div style="padding: 30px;">
            <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin-bottom: 25px;">
                <p style="margin: 0; color: #92400e; font-weight: 500;">
                    ⏰ This is a friendly reminder that you have an appointment scheduled in {days_until} day(s). Please mark your calendar!
                </p>
            </div>
            
            <h2 style="color: #1f2937; margin-bottom: 20px;">Your Appointment Details</h2>
            
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
            
            <div style="background-color: #fee2e2; border: 2px solid #dc2626; padding: 20px; border-radius: 6px; margin-bottom: 25px;">
                <h3 style="color: #991b1b; margin-top: 0; margin-bottom: 10px;">🔒 IMPORTANT: 3-Day Lock Policy</h3>
                <p style="margin: 0; color: #7f1d1d; font-weight: 500; line-height: 1.6;">
                    Your appointment is now within the 3-day lock period. <strong>Cancellation and rescheduling are no longer permitted.</strong> Please ensure you attend your scheduled appointment.
                </p>
            </div>
            
            <div style="background-color: #f0fdf4; padding: 20px; border-radius: 6px; margin-bottom: 25px;">
                <h3 style="color: #166534; margin-top: 0; margin-bottom: 10px;">📋 Preparation Checklist:</h3>
                <ul style="margin: 0; padding-left: 20px; color: #166534;">
                    <li style="margin-bottom: 8px;">Arrive 10 minutes before your scheduled time</li>
                    <li style="margin-bottom: 8px;">Bring valid ID for verification</li>
                    <li style="margin-bottom: 8px;">List any medications you're currently taking</li>
                    <li style="margin-bottom: 8px;">Bring any relevant medical records</li>
                    <li style="margin-bottom: 0;">Wear comfortable clothing for examination</li>
                </ul>
            </div>
            
            <div style="background-color: #f9fafb; padding: 20px; border-radius: 6px; margin-bottom: 25px;">
                <h3 style="color: #1f2937; margin-top: 0; margin-bottom: 10px;">📍 Clinic Information:</h3>
                <p style="margin: 0; color: #4b5563; line-height: 1.6;">
                    <strong>Norzagaray College Clinic</strong><br>
                    Norzagaray, Bulacan<br>
                    Operating hours: Monday - Friday, 8:00 AM - 5:00 PM
                </p>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <p style="color: #6b7280; font-size: 14px; margin: 0;">
                    This is an automated reminder from the iClinic Management System.<br>
                    Please do not reply to this email. For urgent matters, contact the clinic directly.
                </p>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-radius: 0 0 8px 8px; border-top: 1px solid #e5e7eb;">
            <p style="margin: 0; color: #6b7280; font-size: 12px;">
                iClinic Management System • Norzagaray College<br>
                Reminder sent on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </p>
        </div>
    </div>
</body>
</html>
        """
        
        # Send email
        cfg = EMAIL_CONFIG
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{cfg['from_name']} <{cfg['email']}>"
        msg['To'] = patient_email
        msg.attach(MIMEText(html_content, 'html'))
        
        # Connect to SMTP server
        server = smtplib.SMTP(cfg['smtp_server'], cfg['smtp_port'])
        server.starttls()
        server.login(cfg['email'], cfg['password'])
        server.send_message(msg)
        server.quit()
        
        print(f"3-day reminder sent to: {patient_email}")
        return True
        
    except Exception as e:
        print(f"Error sending 3-day reminder: {e}")
        return False

def get_patient_email(patient_name):
    """Get patient email from database"""
    conn = DatabaseConfig.get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    
    try:
        # Try to get email from users table first (for logged-in users)
        cursor.execute('SELECT email FROM users WHERE CONCAT(first_name, " ", last_name) = %s', (patient_name,))
        user_result = cursor.fetchone()
        
        if user_result and user_result[0]:
            return user_result[0].strip()
        
        # Try students table
        cursor.execute('SELECT std_EmailAdd FROM students WHERE CONCAT(std_Firstname, " ", std_Surname) = %s', (patient_name,))
        student_result = cursor.fetchone()
        
        if student_result and student_result[0]:
            return student_result[0].strip()
        
        return None
        
    except Exception as e:
        print(f"Error getting patient email: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Test the notification system
    print("Testing Patient Notification System...")
    print("=" * 60)
    
    # Test booking confirmation
    test_patient = {
        'email': 'test@example.com',
        'name': 'Juan Dela Cruz',
        'date': '2026-04-05',
        'time': '10:30',
        'type': 'General Consultation'
    }
    
    print(f"Sending booking confirmation to: {test_patient['email']}")
    success1 = send_booking_confirmation(
        test_patient['email'], 
        test_patient['name'], 
        test_patient['date'], 
        test_patient['time'], 
        test_patient['type']
    )
    
    # Test 3-day reminder
    print(f"Sending 3-day reminder to: {test_patient['email']}")
    success2 = send_three_day_reminder(
        test_patient['email'], 
        test_patient['name'], 
        test_patient['date'], 
        test_patient['time'], 
        test_patient['type']
    )
    
    if success1 and success2:
        print("\nAll tests completed successfully!")
    else:
        print("\nSome tests failed!")

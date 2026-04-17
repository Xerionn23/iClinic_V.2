"""
Appointment Lock Notification Service for iClinic
Sends email alerts to clinic nurses when appointments become non-cancellable/non-reschedulable (within 3 days)
"""

import smtplib
import os
import io
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from config.database import DatabaseConfig

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'norzagaraycollege.clinic@gmail.com',
    'password': 'xtsweijcxsntwhld',
    'from_name': 'iClinic Management System'
}


def _get_public_base_url() -> str:
    base = (os.environ.get('ICLINIC_PUBLIC_BASE_URL') or '').strip()
    if base:
        return base.rstrip('/')
    return 'http://127.0.0.1:5000'


def _get_qr_token_secret() -> str:
    return (
        (os.environ.get('ICLINIC_QR_TOKEN_SECRET') or '').strip()
        or (os.environ.get('ICLINIC_SECRET_KEY') or '').strip()
        or 'your-secret-key-change-this-in-production'
    )


def _appointment_qr_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(_get_qr_token_secret(), salt='iclinic-appointment-qr-v1')


def _build_appointment_verification_url(appointment_id, patient_name, appointment_date, appointment_time) -> str | None:
    if not appointment_id:
        return None

    token = _appointment_qr_serializer().dumps({
        'aid': int(appointment_id),
        'p': patient_name,
        'd': appointment_date,
        't': appointment_time,
    })
    return f"{_get_public_base_url()}/verify/appointment/{token}"


def _make_qr_png_bytes(data: str) -> bytes | None:
    try:
        import qrcode
    except Exception:
        return None


def _qr_image_url(data: str) -> str:
    encoded = urllib.parse.quote(data, safe='')
    return f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={encoded}"

    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color='black', back_color='white')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()
    except Exception:
        return None

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
        appointment_id = appointment_data.get('id')
        
        appointment_date_str = appointment_date.strftime('%Y-%m-%d') if hasattr(appointment_date, 'strftime') else str(appointment_date or '')
        appointment_time_str = str(appointment_time or '')
        if len(appointment_time_str) >= 5 and appointment_time_str[2] == ':':
            appointment_time_str = appointment_time_str[:5]

        # Format date for display
        try:
            date_obj = datetime.strptime(appointment_date_str, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
        except:
            formatted_date = appointment_date_str
        
        # Format time to 12-hour format
        try:
            time_obj = datetime.strptime(appointment_time_str, '%H:%M')
            formatted_time = time_obj.strftime('%I:%M %p')
        except:
            formatted_time = appointment_time_str
        
        # Create email content
        subject = f"Appointment Within 3 Days: {patient_name} - {formatted_date}"

        verification_url = _build_appointment_verification_url(
            appointment_id=appointment_id,
            patient_name=patient_name,
            appointment_date=appointment_date_str,
            appointment_time=appointment_time_str,
        )
        qr_png = _make_qr_png_bytes(verification_url) if verification_url else None

        if verification_url and qr_png:
            qr_section_html = f"""
            <!-- Appointment QR Code -->
            <div style=\"background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 18px; margin-bottom: 25px;\">
                <p style=\"margin: 0 0 10px 0; color: #1e40af; font-size: 14px; font-weight: 700;\">Appointment QR Code</p>
                <p style=\"margin: 0; color: #374151; font-size: 13px; line-height: 1.5;\">Scan to open the appointment verification page.</p>
                <div style=\"text-align: center; margin-top: 14px;\">
                    <img src=\"cid:appointment_qr\" alt=\"Appointment QR Code\" style=\"width: 220px; height: 220px; border: 1px solid #e5e7eb; border-radius: 8px;\" />
                </div>
                <p style=\"margin: 14px 0 0 0; color: #6b7280; font-size: 12px; word-break: break-all;\">
                    Verification link: <a href=\"{verification_url}\" style=\"color:#2563eb;\">{verification_url}</a>
                </p>
            </div>
            """
        elif verification_url:
            qr_section_html = f"""
            <!-- Appointment QR Code (Hosted) -->
            <div style=\"background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 18px; margin-bottom: 25px;\">
                <p style=\"margin: 0 0 10px 0; color: #1e40af; font-size: 14px; font-weight: 700;\">Appointment QR Code</p>
                <p style=\"margin: 0; color: #374151; font-size: 13px; line-height: 1.5;\">Scan to open the appointment verification page.</p>
                <div style=\"text-align: center; margin-top: 14px;\">
                    <img src=\"{_qr_image_url(verification_url)}\" alt=\"Appointment QR Code\" style=\"width: 220px; height: 220px; border: 1px solid #e5e7eb; border-radius: 8px;\" />
                </div>
                <p style=\"margin: 14px 0 0 0; color: #6b7280; font-size: 12px; word-break: break-all;\">
                    Verification link: <a href=\"{verification_url}\" style=\"color:#2563eb;\">{verification_url}</a>
                </p>
            </div>
            """
        else:
            qr_section_html = ""
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointment Within 3 Days Notice</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: 'Inter', Arial, sans-serif;">
    <div style="max-width: 600px; margin: 20px auto; background-color: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden;">
        <!-- Blue Header -->
        <div style="background-color: #2563eb; color: white; padding: 30px 20px; text-align: center;">
            <h1 style="margin: 0; font-size: 24px; font-weight: bold;">iClinic Management System</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 14px;">Norzagaray College</p>
        </div>
        
        <!-- Content -->
        <div style="padding: 40px 30px;">
            <h2 style="color: #dc2626; margin: 0 0 20px 0; font-size: 22px;">Appointment Within 3 Days</h2>
            
            <p style="color: #374151; margin: 0 0 20px 0; line-height: 1.6;">
                Hello,
            </p>
            
            <p style="color: #374151; margin: 0 0 25px 0; line-height: 1.6;">
                This appointment is within 3 days and changes must be coordinated with the clinic per policy.
            </p>
            
            <!-- Appointment Details Box -->
            <div style="background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
                <p style="margin: 0 0 12px 0; font-size: 14px; color: #374151;">
                    <strong>Patient Name:</strong> {patient_name}
                </p>
                <p style="margin: 0 0 12px 0; font-size: 14px; color: #374151;">
                    <strong>Date:</strong> {formatted_date}
                </p>
                <p style="margin: 0 0 12px 0; font-size: 14px; color: #374151;">
                    <strong>Time:</strong> {formatted_time}
                </p>
                <p style="margin: 0; font-size: 14px; color: #374151;">
                    <strong>Type:</strong> {appointment_type}
                </p>
            </div>
            
            <!-- Important Notice -->
            <div style="background-color: #fee2e2; border-left: 4px solid #dc2626; padding: 15px; margin-bottom: 25px;">
                <p style="margin: 0; color: #991b1b; font-size: 14px; line-height: 1.5;">
                    <strong>Important:</strong> This appointment is in the final 3-day change window. Cancellation or rescheduling is no longer available. Please ensure the patient attends the scheduled appointment.
                </p>
            </div>

            {qr_section_html}
            
            <!-- Button -->
            <div style="text-align: center; margin-bottom: 25px;">
                <a href="http://127.0.0.1:5000" 
                   style="display: inline-block; background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 500;">
                    View Appointment
                </a>
            </div>
            
            <p style="color: #6b7280; font-size: 13px; margin: 0 0 10px 0;">
                If the button doesn't work, copy and paste this link into your browser:
            </p>
            <p style="margin: 0;">
                <a href="http://127.0.0.1:5000" style="color: #2563eb; font-size: 13px; word-break: break-all;">http://127.0.0.1:5000</a>
            </p>
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb;">
            <p style="margin: 0; color: #6b7280; font-size: 12px; line-height: 1.5;">
                © 2024 iClinic Management System<br>
                Norzagaray College<br>
                If you need assistance, please contact IT support.
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
                msg = MIMEMultipart('related')
                msg['Subject'] = subject
                msg['From'] = f"{cfg['from_name']} <{cfg['email']}>"
                msg['To'] = nurse_email

                html_part = MIMEMultipart('alternative')
                html_part.attach(MIMEText(html_content, 'html'))
                msg.attach(html_part)

                if qr_png:
                    qr_image = MIMEImage(qr_png, _subtype='png')
                    qr_image.add_header('Content-ID', '<appointment_qr>')
                    qr_image.add_header('Content-Disposition', 'inline', filename='appointment_qr.png')
                    msg.attach(qr_image)
                
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

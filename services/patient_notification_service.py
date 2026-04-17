"""
Patient Notification Service for iClinic
Sends email notifications to patients:
1. Booking confirmation (immediate)
2. 3-day reminder before appointment
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


def _build_appointment_verification_url(appointment_id: int | None, patient_name: str, appointment_date: str, appointment_time: str) -> str | None:
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


def send_booking_confirmation(patient_email, patient_name, appointment_date, appointment_time, appointment_type, appointment_id=None):
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

        home_url = _get_public_base_url()
        verification_url = _build_appointment_verification_url(
            appointment_id=appointment_id,
            patient_name=patient_name,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        )
        qr_png = _make_qr_png_bytes(verification_url) if verification_url else None

        if verification_url and qr_png:
            qr_section_html = f"""
            <!-- Appointment QR Code -->
            <div style=\"background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 18px; margin-bottom: 25px;\">
                <p style=\"margin: 0 0 10px 0; color: #1e40af; font-size: 14px; font-weight: 700;\">Clinic QR Code</p>
                <p style=\"margin: 0; color: #374151; font-size: 13px; line-height: 1.5;\">Show this QR code at the clinic for quick verification.</p>
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
                <p style=\"margin: 0 0 10px 0; color: #1e40af; font-size: 14px; font-weight: 700;\">Clinic QR Code</p>
                <p style=\"margin: 0; color: #374151; font-size: 13px; line-height: 1.5;\">Show this QR code at the clinic for quick verification.</p>
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
    <title>Appointment Confirmation</title>
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
            <h2 style="color: #1e40af; margin: 0 0 20px 0; font-size: 22px;">Appointment Confirmed</h2>
            
            <p style="color: #374151; margin: 0 0 20px 0; line-height: 1.6;">
                Hello {patient_name},
            </p>
            
            <p style="color: #374151; margin: 0 0 25px 0; line-height: 1.6;">
                Your appointment has been successfully scheduled with the iClinic Management System.
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
            
            {qr_section_html}
            
            <!-- Important Notice -->
            <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin-bottom: 25px;">
                <p style="margin: 0; color: #92400e; font-size: 14px; line-height: 1.5;">
                    <strong>Important:</strong> Please arrive 10 minutes before your scheduled time. Bring a valid ID for verification.
                </p>
            </div>
            
            <!-- Button -->
            <div style="text-align: center; margin-bottom: 25px;">
                <a href="http://127.0.0.1:5000" 
                   style="display: inline-block; background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 500;">
                    View Your Appointment
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
        
        # Send email
        cfg = EMAIL_CONFIG

        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = f"{cfg['from_name']} <{cfg['email']}>"
        msg['To'] = patient_email

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
        
        print(f"Booking confirmation sent to: {patient_email}")
        return True
        
    except Exception as e:
        print(f"Error sending booking confirmation: {e}")
        return False

def send_three_day_reminder(patient_email, patient_name, appointment_date, appointment_time, appointment_type, appointment_id=None):
    """Send 3-day reminder email to patient"""
    try:
        # Format appointment date and time
        try:
            date_obj = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            formatted_date = date_obj.strftime('%B %d, %Y')
            days_until = (date_obj - datetime.now().date()).days
        except Exception:
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

        home_url = _get_public_base_url()
        verification_url = _build_appointment_verification_url(
            appointment_id=appointment_id,
            patient_name=patient_name,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        )
        qr_png = _make_qr_png_bytes(verification_url) if verification_url else None

        if verification_url and qr_png:
            qr_section_html = f"""
            <!-- Appointment QR Code -->
            <div style=\"background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 18px; margin-bottom: 25px;\">
                <p style=\"margin: 0 0 10px 0; color: #1e40af; font-size: 14px; font-weight: 700;\">Clinic QR Code</p>
                <p style=\"margin: 0; color: #374151; font-size: 13px; line-height: 1.5;\">Show this QR code at the clinic for quick verification.</p>
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
                <p style=\"margin: 0 0 10px 0; color: #1e40af; font-size: 14px; font-weight: 700;\">Clinic QR Code</p>
                <p style=\"margin: 0; color: #374151; font-size: 13px; line-height: 1.5;\">Show this QR code at the clinic for quick verification.</p>
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
    <title>Appointment Reminder</title>
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
            <h2 style="color: #1e40af; margin: 0 0 20px 0; font-size: 22px;">Appointment Reminder</h2>
            
            <p style="color: #374151; margin: 0 0 20px 0; line-height: 1.6;">
                Hello {patient_name},
            </p>
            
            <p style="color: #374151; margin: 0 0 25px 0; line-height: 1.6;">
                This is a friendly reminder that you have an appointment scheduled in {days_until} day(s).
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
            
            {qr_section_html}
            
            <!-- Important Notice - 3-Day Change Window -->
            <div style="background-color: #fee2e2; border-left: 4px solid #dc2626; padding: 15px; margin-bottom: 25px;">
                <p style="margin: 0; color: #991b1b; font-size: 14px; line-height: 1.5;">
                    <strong>Important:</strong> Your appointment is within the final 3-day change window. Cancellation and rescheduling are no longer available. Please contact the clinic if you need assistance.
                </p>
            </div>
            
            <!-- Preparation Checklist -->
            <div style="background-color: #f0fdf4; border-left: 4px solid #10b981; padding: 15px; margin-bottom: 25px;">
                <p style="margin: 0 0 10px 0; color: #166534; font-size: 14px; font-weight: 600;">
                    Preparation Checklist:
                </p>
                <ul style="margin: 0; padding-left: 20px; color: #166534; font-size: 14px; line-height: 1.6;">
                    <li>Arrive 10 minutes before your scheduled time</li>
                    <li>Bring valid ID for verification</li>
                    <li>List any medications you're currently taking</li>
                    <li>Bring any relevant medical records</li>
                    <li>Wear comfortable clothing for examination</li>
                </ul>
            </div>
            
            <!-- Button -->
            <div style="text-align: center; margin-bottom: 25px;">
                <a href="http://127.0.0.1:5000" 
                   style="display: inline-block; background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 500;">
                    View Your Appointment
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
        
        # Send email
        cfg = EMAIL_CONFIG

        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = f"{cfg['from_name']} <{cfg['email']}>"
        msg['To'] = patient_email

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

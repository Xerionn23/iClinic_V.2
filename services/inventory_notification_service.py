"""
Inventory Notification Service for iClinic
Sends email alerts to nurses about medicine inventory status:
- Medicines expiring in 60 days
- Medicines expiring in 30 days
- Medicines with low stock (10 or less)
- Expired medicines
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
    'from_name': 'iClinic Inventory System'
}

def get_inventory_alerts():
    """
    Check medicine inventory and return alerts for:
    - Expiring in 60 days
    - Expiring in 30 days
    - Low stock (10 or less)
    - Already expired
    """
    conn = DatabaseConfig.get_connection()
    if not conn:
        print("❌ Database connection failed")
        return None
    
    cursor = conn.cursor()
    today = datetime.now().date()
    days_60 = today + timedelta(days=60)
    days_30 = today + timedelta(days=30)
    
    alerts = {
        'expiring_60_days': [],
        'expiring_30_days': [],
        'low_stock': [],
        'expired': []
    }
    
    try:
        # Get all medicines with their batches
        cursor.execute('''
            SELECT 
                m.medicine_id,
                m.medicine_name,
                m.category,
                m.quantity_in_stock,
                mb.id as batch_id,
                mb.quantity as batch_quantity,
                mb.expiry_date
            FROM medicines m
            LEFT JOIN medicine_batches mb ON m.medicine_id = mb.medicine_id
            WHERE mb.status = 'available' AND mb.quantity > 0
            ORDER BY m.medicine_name, mb.expiry_date
        ''')
        
        medicines_data = cursor.fetchall()
        
        # Process each batch
        for row in medicines_data:
            medicine_id, medicine_name, category, total_stock, batch_id, batch_qty, expiry_date = row
            
            # Check expiry dates
            if expiry_date:
                if expiry_date <= today:
                    # Already expired
                    alerts['expired'].append({
                        'medicine_name': medicine_name,
                        'quantity': batch_qty,
                        'expiry_date': expiry_date.strftime('%Y-%m-%d'),
                        'days_overdue': (today - expiry_date).days
                    })
                elif expiry_date <= days_30:
                    # Expiring in 30 days or less
                    days_until_expiry = (expiry_date - today).days
                    alerts['expiring_30_days'].append({
                        'medicine_name': medicine_name,
                        'quantity': batch_qty,
                        'expiry_date': expiry_date.strftime('%Y-%m-%d'),
                        'days_until_expiry': days_until_expiry
                    })
                elif expiry_date <= days_60:
                    # Expiring in 60 days or less
                    days_until_expiry = (expiry_date - today).days
                    alerts['expiring_60_days'].append({
                        'medicine_name': medicine_name,
                        'quantity': batch_qty,
                        'expiry_date': expiry_date.strftime('%Y-%m-%d'),
                        'days_until_expiry': days_until_expiry
                    })
        
        # Check for low stock medicines (total stock across all batches)
        cursor.execute('''
            SELECT 
                m.medicine_id,
                m.medicine_name,
                m.category,
                m.quantity_in_stock
            FROM medicines m
            WHERE m.quantity_in_stock <= 10 AND m.quantity_in_stock > 0
        ''')
        
        low_stock_data = cursor.fetchall()
        for row in low_stock_data:
            medicine_id, medicine_name, category, total_stock = row
            alerts['low_stock'].append({
                'medicine_name': medicine_name,
                'category': category or 'N/A',
                'total_stock': total_stock
            })
        
        cursor.close()
        conn.close()
        
        return alerts
        
    except Exception as e:
        print(f"❌ Error getting inventory alerts: {e}")
        cursor.close()
        conn.close()
        return None


def create_email_html(alerts):
    """Create HTML email content with all alerts - standardized format"""
    
    # Count total alerts
    total_alerts = (
        len(alerts['expired']) + 
        len(alerts['expiring_30_days']) + 
        len(alerts['expiring_60_days']) + 
        len(alerts['low_stock'])
    )
    
    if total_alerts == 0:
        return None  # No alerts to send
    
    # Build alert sections
    alert_sections = ""
    
    # EXPIRED MEDICINES
    if alerts['expired']:
        expired_rows = ""
        for item in alerts['expired']:
            expired_rows += f"""
                    <tr>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><strong>{item['medicine_name']}</strong></td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><span style="display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; background: #fee2e2; color: #dc2626;">{item['quantity']} units</span></td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;">{item['expiry_date']}</td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><span style="display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; background: #fee2e2; color: #dc2626;">{item['days_overdue']} days</span></td>
                    </tr>"""
        alert_sections += f"""
            <!-- Expired Section -->
            <div style="margin-bottom: 30px;">
                <div style="background: #fef2f2; padding: 15px; border-left: 4px solid #dc2626; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #dc2626; font-size: 18px;">🚨 EXPIRED MEDICINES</h3>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">These medicines have already expired and should be removed immediately</p>
                </div>
                <table style="width: 100%; border-collapse: collapse; background: white; border: 1px solid #e5e7eb; border-radius: 8px;">
                    <thead>
                        <tr style="background: #f9fafb;">
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Medicine Name</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Quantity</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Expired Date</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Days Overdue</th>
                        </tr>
                    </thead>
                    <tbody>{expired_rows}</tbody>
                </table>
            </div>"""
    
    # EXPIRING IN 30 DAYS
    if alerts['expiring_30_days']:
        expiring_rows = ""
        for item in alerts['expiring_30_days']:
            expiring_rows += f"""
                    <tr>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><strong>{item['medicine_name']}</strong></td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><span style="display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; background: #fef3c7; color: #d97706;">{item['quantity']} units</span></td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;">{item['expiry_date']}</td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><span style="display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; background: #fef3c7; color: #d97706;">{item['days_until_expiry']} days</span></td>
                    </tr>"""
        alert_sections += f"""
            <!-- Expiring 30 Days Section -->
            <div style="margin-bottom: 30px;">
                <div style="background: #fef3c7; padding: 15px; border-left: 4px solid #f59e0b; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #d97706; font-size: 18px;">⚠️ EXPIRING IN 30 DAYS</h3>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">These medicines will expire within 30 days. Plan usage or replacement soon</p>
                </div>
                <table style="width: 100%; border-collapse: collapse; background: white; border: 1px solid #e5e7eb; border-radius: 8px;">
                    <thead>
                        <tr style="background: #f9fafb;">
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Medicine Name</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Quantity</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Expiry Date</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Days Until</th>
                        </tr>
                    </thead>
                    <tbody>{expiring_rows}</tbody>
                </table>
            </div>"""
    
    # EXPIRING IN 60 DAYS
    if alerts['expiring_60_days']:
        expiring60_rows = ""
        for item in alerts['expiring_60_days']:
            expiring60_rows += f"""
                    <tr>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><strong>{item['medicine_name']}</strong></td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><span style="display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; background: #dbeafe; color: #2563eb;">{item['quantity']} units</span></td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;">{item['expiry_date']}</td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><span style="display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; background: #dbeafe; color: #2563eb;">{item['days_until_expiry']} days</span></td>
                    </tr>"""
        alert_sections += f"""
            <!-- Expiring 60 Days Section -->
            <div style="margin-bottom: 30px;">
                <div style="background: #dbeafe; padding: 15px; border-left: 4px solid #2563eb; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #2563eb; font-size: 18px;">📅 EXPIRING IN 60 DAYS</h3>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">These medicines will expire within 60 days. Monitor usage and plan accordingly</p>
                </div>
                <table style="width: 100%; border-collapse: collapse; background: white; border: 1px solid #e5e7eb; border-radius: 8px;">
                    <thead>
                        <tr style="background: #f9fafb;">
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Medicine Name</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Quantity</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Expiry Date</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Days Until</th>
                        </tr>
                    </thead>
                    <tbody>{expiring60_rows}</tbody>
                </table>
            </div>"""
    
    # LOW STOCK
    if alerts['low_stock']:
        lowstock_rows = ""
        for item in alerts['low_stock']:
            lowstock_rows += f"""
                    <tr>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><strong>{item['medicine_name']}</strong></td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;">{item['category']}</td>
                        <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #374151;"><span style="display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; background: #fef3c7; color: #d97706;">{item['total_stock']} units</span></td>
                    </tr>"""
        alert_sections += f"""
            <!-- Low Stock Section -->
            <div style="margin-bottom: 30px;">
                <div style="background: #fef3c7; padding: 15px; border-left: 4px solid #f59e0b; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #d97706; font-size: 18px;">📦 LOW STOCK ALERT</h3>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">These medicines have 10 or fewer units in stock. Consider reordering</p>
                </div>
                <table style="width: 100%; border-collapse: collapse; background: white; border: 1px solid #e5e7eb; border-radius: 8px;">
                    <thead>
                        <tr style="background: #f9fafb;">
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Medicine Name</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Category</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 14px; color: #374151;">Current Stock</th>
                        </tr>
                    </thead>
                    <tbody>{lowstock_rows}</tbody>
                </table>
            </div>"""
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventory Alert</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: 'Inter', Arial, sans-serif;">
    <div style="max-width: 800px; margin: 20px auto; background-color: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden;">
        <!-- Blue Header -->
        <div style="background-color: #2563eb; color: white; padding: 30px 20px; text-align: center;">
            <h1 style="margin: 0; font-size: 24px; font-weight: bold;">iClinic Management System</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 14px;">Norzagaray College</p>
        </div>
        
        <!-- Content -->
        <div style="padding: 40px 30px;">
            <h2 style="color: #1e40af; margin: 0 0 20px 0; font-size: 22px;">🏥 Inventory Alert</h2>
            
            <p style="color: #374151; margin: 0 0 20px 0; line-height: 1.6;">
                Hello,
            </p>
            
            <p style="color: #374151; margin: 0 0 25px 0; line-height: 1.6;">
                This is an automated alert regarding the current status of medicine inventory. Please review the details below and take appropriate action.
            </p>
            
            <!-- Summary Box -->
            <div style="background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 25px;">
                <h3 style="margin: 0 0 15px 0; color: #dc2626; font-size: 18px;">� Alert Summary</h3>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                    <div style="background: white; padding: 15px; border-radius: 6px; border-left: 3px solid #dc2626;">
                        <p style="font-size: 32px; font-weight: bold; color: #dc2626; margin: 0;">{len(alerts['expired'])}</p>
                        <p style="color: #666; font-size: 14px; margin: 5px 0 0 0;">Expired Medicines</p>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 6px; border-left: 3px solid #f59e0b;">
                        <p style="font-size: 32px; font-weight: bold; color: #d97706; margin: 0;">{len(alerts['expiring_30_days'])}</p>
                        <p style="color: #666; font-size: 14px; margin: 5px 0 0 0;">Expiring in 30 Days</p>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 6px; border-left: 3px solid #2563eb;">
                        <p style="font-size: 32px; font-weight: bold; color: #2563eb; margin: 0;">{len(alerts['expiring_60_days'])}</p>
                        <p style="color: #666; font-size: 14px; margin: 5px 0 0 0;">Expiring in 60 Days</p>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 6px; border-left: 3px solid #f59e0b;">
                        <p style="font-size: 32px; font-weight: bold; color: #d97706; margin: 0;">{len(alerts['low_stock'])}</p>
                        <p style="color: #666; font-size: 14px; margin: 5px 0 0 0;">Low Stock Items</p>
                    </div>
                </div>
            </div>
            
            {alert_sections}
            
            <!-- Action Required -->
            <div style="background-color: #fef2f2; border: 2px solid #dc2626; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="margin: 0 0 10px 0; color: #dc2626;">📋 Action Required</h3>
                <p style="margin: 0 0 10px 0; color: #374151;"><strong>Please review the inventory alerts above and take appropriate action:</strong></p>
                <ul style="margin: 0; padding-left: 20px; color: #374151; line-height: 1.6;">
                    <li>Remove expired medicines from inventory immediately</li>
                    <li>Plan usage for medicines expiring soon</li>
                    <li>Reorder low stock items to maintain adequate supply</li>
                    <li>Update inventory records in the iClinic Management System</li>
                </ul>
            </div>
            
            <!-- Button -->
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:5000" 
                   style="display: inline-block; background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 500;">
                    View Inventory Dashboard
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
</html>"""
    
    return html


def send_inventory_notification_email(to_emails):
    """
    Send consolidated inventory notification email to nurses
    
    Args:
        to_emails: List of nurse email addresses or single email string
    """
    # Get inventory alerts
    alerts = get_inventory_alerts()
    
    if not alerts:
        print("❌ Failed to get inventory alerts")
        return False
    
    # Check if there are any alerts
    total_alerts = (
        len(alerts['expired']) + 
        len(alerts['expiring_30_days']) + 
        len(alerts['expiring_60_days']) + 
        len(alerts['low_stock'])
    )
    
    if total_alerts == 0:
        print("✅ No inventory alerts to send")
        return True
    
    # Create email HTML
    html_content = create_email_html(alerts)
    
    if not html_content:
        print("✅ No alerts to send")
        return True
    
    # Ensure to_emails is a list
    if isinstance(to_emails, str):
        to_emails = [to_emails]
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🚨 iClinic Inventory Alert - {total_alerts} Items Need Attention"
        msg['From'] = f"{EMAIL_CONFIG['from_name']} <{EMAIL_CONFIG['email']}>"
        msg['To'] = ', '.join(to_emails)
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        
        print(f"✅ Inventory notification email sent successfully to {len(to_emails)} recipient(s)")
        print(f"   📊 Total alerts: {total_alerts}")
        print(f"   🚨 Expired: {len(alerts['expired'])}")
        print(f"   ⚠️  Expiring in 30 days: {len(alerts['expiring_30_days'])}")
        print(f"   📅 Expiring in 60 days: {len(alerts['expiring_60_days'])}")
        print(f"   📦 Low stock: {len(alerts['low_stock'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sending inventory notification email: {e}")
        return False


def get_nurse_emails():
    """Get nurse email addresses - returns system email"""
    # Always send to the clinic system email
    system_email = 'norzagaraycollege.clinic@gmail.com'
    print(f"✅ Using clinic system email: {system_email}")
    return [system_email]


if __name__ == "__main__":
    # Test the notification system
    print("🧪 Testing Inventory Notification System...")
    print("=" * 60)
    
    # Get nurse emails
    nurse_emails = get_nurse_emails()
    
    if not nurse_emails:
        print("⚠️ No nurse emails found. Using test email...")
        nurse_emails = ['norzagaraycollege.clinic@gmail.com']
    
    # Send notification
    success = send_inventory_notification_email(nurse_emails)
    
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")

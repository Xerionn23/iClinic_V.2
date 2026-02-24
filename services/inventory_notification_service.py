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
    """Create HTML email content with all alerts"""
    
    # Count total alerts
    total_alerts = (
        len(alerts['expired']) + 
        len(alerts['expiring_30_days']) + 
        len(alerts['expiring_60_days']) + 
        len(alerts['low_stock'])
    )
    
    if total_alerts == 0:
        return None  # No alerts to send
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; }}
            .header {{ background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); color: white; padding: 30px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .header p {{ margin: 10px 0 0 0; font-size: 16px; opacity: 0.9; }}
            .content {{ padding: 30px; }}
            .alert-section {{ margin-bottom: 30px; }}
            .alert-header {{ background: #f8f9fa; padding: 15px; border-left: 4px solid #dc2626; margin-bottom: 15px; }}
            .alert-header h2 {{ margin: 0; color: #dc2626; font-size: 20px; }}
            .alert-header p {{ margin: 5px 0 0 0; color: #666; font-size: 14px; }}
            .alert-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            .alert-table th {{ background: #f8f9fa; padding: 12px; text-align: left; border-bottom: 2px solid #dee2e6; font-size: 14px; }}
            .alert-table td {{ padding: 12px; border-bottom: 1px solid #dee2e6; font-size: 14px; }}
            .alert-table tr:hover {{ background: #f8f9fa; }}
            .badge {{ display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
            .badge-danger {{ background: #fee2e2; color: #dc2626; }}
            .badge-warning {{ background: #fef3c7; color: #d97706; }}
            .badge-info {{ background: #dbeafe; color: #2563eb; }}
            .summary {{ background: #fef2f2; border: 1px solid #fecaca; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
            .summary h3 {{ margin: 0 0 15px 0; color: #dc2626; }}
            .summary-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }}
            .summary-item {{ background: white; padding: 15px; border-radius: 6px; border-left: 3px solid #dc2626; }}
            .summary-item .number {{ font-size: 32px; font-weight: bold; color: #dc2626; margin: 0; }}
            .summary-item .label {{ color: #666; font-size: 14px; margin: 5px 0 0 0; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 12px; }}
            .action-required {{ background: #fef2f2; border: 2px solid #dc2626; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            .action-required h3 {{ margin: 0 0 10px 0; color: #dc2626; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 iClinic Inventory Alert</h1>
                <p>Medicine Inventory Status Report - {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="content">
                <div class="summary">
                    <h3>📊 Alert Summary</h3>
                    <div class="summary-grid">
                        <div class="summary-item">
                            <p class="number">{len(alerts['expired'])}</p>
                            <p class="label">Expired Medicines</p>
                        </div>
                        <div class="summary-item">
                            <p class="number">{len(alerts['expiring_30_days'])}</p>
                            <p class="label">Expiring in 30 Days</p>
                        </div>
                        <div class="summary-item">
                            <p class="number">{len(alerts['expiring_60_days'])}</p>
                            <p class="label">Expiring in 60 Days</p>
                        </div>
                        <div class="summary-item">
                            <p class="number">{len(alerts['low_stock'])}</p>
                            <p class="label">Low Stock Items</p>
                        </div>
                    </div>
                </div>
    """
    
    # EXPIRED MEDICINES (Highest Priority)
    if alerts['expired']:
        html += """
                <div class="alert-section">
                    <div class="alert-header">
                        <h2>🚨 EXPIRED MEDICINES - IMMEDIATE ACTION REQUIRED</h2>
                        <p>These medicines have already expired and should be removed from inventory immediately</p>
                    </div>
                    <table class="alert-table">
                        <thead>
                            <tr>
                                <th>Medicine Name</th>
                                <th>Quantity</th>
                                <th>Expired Date</th>
                                <th>Days Overdue</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        for item in alerts['expired']:
            html += f"""
                            <tr>
                                <td><strong>{item['medicine_name']}</strong></td>
                                <td><span class="badge badge-danger">{item['quantity']} units</span></td>
                                <td>{item['expiry_date']}</td>
                                <td><span class="badge badge-danger">{item['days_overdue']} days</span></td>
                            </tr>
            """
        html += """
                        </tbody>
                    </table>
                </div>
        """
    
    # EXPIRING IN 30 DAYS
    if alerts['expiring_30_days']:
        html += """
                <div class="alert-section">
                    <div class="alert-header">
                        <h2>⚠️ EXPIRING IN 30 DAYS - URGENT ATTENTION NEEDED</h2>
                        <p>These medicines will expire within 30 days. Plan usage or replacement soon</p>
                    </div>
                    <table class="alert-table">
                        <thead>
                            <tr>
                                <th>Medicine Name</th>
                                <th>Quantity</th>
                                <th>Expiry Date</th>
                                <th>Days Until Expiry</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        for item in alerts['expiring_30_days']:
            html += f"""
                            <tr>
                                <td><strong>{item['medicine_name']}</strong></td>
                                <td><span class="badge badge-warning">{item['quantity']} units</span></td>
                                <td>{item['expiry_date']}</td>
                                <td><span class="badge badge-warning">{item['days_until_expiry']} days</span></td>
                            </tr>
            """
        html += """
                        </tbody>
                    </table>
                </div>
        """
    
    # EXPIRING IN 60 DAYS
    if alerts['expiring_60_days']:
        html += """
                <div class="alert-section">
                    <div class="alert-header">
                        <h2>📅 EXPIRING IN 60 DAYS - MONITOR CLOSELY</h2>
                        <p>These medicines will expire within 60 days. Monitor usage and plan accordingly</p>
                    </div>
                    <table class="alert-table">
                        <thead>
                            <tr>
                                <th>Medicine Name</th>
                                <th>Quantity</th>
                                <th>Expiry Date</th>
                                <th>Days Until Expiry</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        for item in alerts['expiring_60_days']:
            html += f"""
                            <tr>
                                <td><strong>{item['medicine_name']}</strong></td>
                                <td><span class="badge badge-info">{item['quantity']} units</span></td>
                                <td>{item['expiry_date']}</td>
                                <td><span class="badge badge-info">{item['days_until_expiry']} days</span></td>
                            </tr>
            """
        html += """
                        </tbody>
                    </table>
                </div>
        """
    
    # LOW STOCK
    if alerts['low_stock']:
        html += """
                <div class="alert-section">
                    <div class="alert-header">
                        <h2>📦 LOW STOCK ALERT - REORDER NEEDED</h2>
                        <p>These medicines have 10 or fewer units in stock. Consider reordering</p>
                    </div>
                    <table class="alert-table">
                        <thead>
                            <tr>
                                <th>Medicine Name</th>
                                <th>Category</th>
                                <th>Current Stock</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        for item in alerts['low_stock']:
            html += f"""
                            <tr>
                                <td><strong>{item['medicine_name']}</strong></td>
                                <td>{item['category']}</td>
                                <td><span class="badge badge-warning">{item['total_stock']} units</span></td>
                            </tr>
            """
        html += """
                        </tbody>
                    </table>
                </div>
        """
    
    html += """
                <div class="action-required">
                    <h3>📋 Action Required</h3>
                    <p><strong>Please review the inventory alerts above and take appropriate action:</strong></p>
                    <ul>
                        <li>Remove expired medicines from inventory immediately</li>
                        <li>Plan usage for medicines expiring soon</li>
                        <li>Reorder low stock items to maintain adequate supply</li>
                        <li>Update inventory records in the iClinic system</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>iClinic Healthcare Management System</strong></p>
                <p>Norzagaray College Clinic</p>
                <p>This is an automated notification. Please do not reply to this email.</p>
                <p>For assistance, contact the clinic administrator.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
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

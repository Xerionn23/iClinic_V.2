"""
Android SMS Gateway Integration Service
FREE SMS sending using local Android device - NO INTERNET REQUIRED!
Works with: https://github.com/capcom6/android-sms-gateway
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AndroidSMSGateway:
    """
    Integrates with Android SMS Gateway app for FREE SMS sending
    Supports both LOCAL (offline) and CLOUD modes
    """
    
    def __init__(self, use_local: bool = True):
        """
        Initialize SMS Gateway connection
        
        Args:
            use_local: True for local server (offline), False for cloud server
        """
        self.use_local = use_local
        
        # Configuration from your screenshot
        if use_local:
            # LOCAL SERVER - Works WITHOUT internet!
            self.base_url = "http://192.168.100.85:8080"
            self.username = "sms"
            self.password = "Qw_Y7IcU"
            self.device_id = "000000004bbc34ed0000019a11c2b"
        else:
            # CLOUD SERVER - Requires internet
            self.base_url = "https://api.sms-gate.app:443"
            self.username = "QYCHOY"
            self.password = "spmcx3gxj6ja6l"
            self.device_id = "Yk9DqOBN5DLplpYAqMibd"
        
        self.headers = {
            'Content-Type': 'application/json'
        }
        
        logger.info(f"📱 Android SMS Gateway initialized ({'LOCAL/OFFLINE' if use_local else 'CLOUD'})")
    
    def send_sms(self, phone_number: str, message: str) -> Dict:
        """
        Send SMS using Android SMS Gateway
        
        Args:
            phone_number: Recipient phone number (e.g., "09557850712")
            message: SMS message content
            
        Returns:
            Dict with status and message_id
        """
        try:
            # Prepare SMS payload according to Android SMS Gateway API
            payload = {
                "message": message,
                "phoneNumbers": [self._format_phone_number(phone_number)]
            }
            
            # Add authentication
            if self.use_local:
                # Local server uses basic auth
                auth = (self.username, self.password)
                response = requests.post(
                    f"{self.base_url}/message",
                    json=payload,
                    headers=self.headers,
                    auth=auth,
                    timeout=10
                )
            else:
                # Cloud server uses token auth
                headers = self.headers.copy()
                headers['Authorization'] = f'Bearer {self.password}'
                response = requests.post(
                    f"{self.base_url}/message",
                    json=payload,
                    headers=headers,
                    timeout=10
                )
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.info(f"✅ SMS sent successfully to {phone_number}")
                return {
                    'success': True,
                    'message_id': result.get('id', 'unknown'),
                    'status': 'sent'
                }
            else:
                logger.error(f"❌ SMS failed: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.ConnectionError:
            logger.error("❌ Cannot connect to Android SMS Gateway. Is the app running?")
            return {
                'success': False,
                'error': 'Connection failed. Check if Android SMS Gateway app is running.'
            }
        except Exception as e:
            logger.error(f"❌ SMS sending error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_bulk_sms(self, recipients: List[Dict[str, str]]) -> Dict:
        """
        Send SMS to multiple recipients
        
        Args:
            recipients: List of dicts with 'phone' and 'message' keys
            
        Returns:
            Dict with success count and failed list
        """
        results = {
            'total': len(recipients),
            'sent': 0,
            'failed': []
        }
        
        for recipient in recipients:
            phone = recipient.get('phone')
            message = recipient.get('message')
            
            if not phone or not message:
                results['failed'].append({
                    'phone': phone,
                    'error': 'Missing phone or message'
                })
                continue
            
            result = self.send_sms(phone, message)
            
            if result['success']:
                results['sent'] += 1
            else:
                results['failed'].append({
                    'phone': phone,
                    'error': result.get('error', 'Unknown error')
                })
        
        logger.info(f"📊 Bulk SMS: {results['sent']}/{results['total']} sent successfully")
        return results
    
    def _format_phone_number(self, phone: str) -> str:
        """
        Format phone number for SMS gateway
        Converts 09557850712 to +639171234567
        """
        phone = phone.strip().replace(' ', '').replace('-', '')
        
        # If starts with 0, replace with +63
        if phone.startswith('0'):
            phone = '+63' + phone[1:]
        # If doesn't start with +, add +63
        elif not phone.startswith('+'):
            phone = '+63' + phone
        
        return phone
    
    def check_status(self) -> Dict:
        """
        Check if SMS Gateway is online and accessible
        
        Returns:
            Dict with status information
        """
        try:
            if self.use_local:
                auth = (self.username, self.password)
                response = requests.get(
                    f"{self.base_url}/health",
                    auth=auth,
                    timeout=5
                )
            else:
                headers = self.headers.copy()
                headers['Authorization'] = f'Bearer {self.password}'
                response = requests.get(
                    f"{self.base_url}/health",
                    headers=headers,
                    timeout=5
                )
            
            if response.status_code == 200:
                return {
                    'online': True,
                    'mode': 'LOCAL (Offline)' if self.use_local else 'CLOUD',
                    'server': self.base_url
                }
            else:
                return {
                    'online': False,
                    'error': f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                'online': False,
                'error': str(e)
            }


class InventorySMSNotifier:
    """
    Handles SMS notifications for inventory alerts
    Integrates AI predictions with SMS sending
    """
    
    def __init__(self, sms_gateway: AndroidSMSGateway):
        self.sms = sms_gateway
        self.admin_phones = []  # Will be loaded from database
    
    def set_admin_phones(self, phone_numbers: List[str]):
        """Set admin phone numbers for notifications"""
        self.admin_phones = phone_numbers
        logger.info(f"📱 Admin phones configured: {len(phone_numbers)} numbers")
    
    def send_low_stock_alert(self, medicine_name: str, current_stock: int, 
                            predicted_days: int, reorder_point: int) -> Dict:
        """
        Send SMS alert for low stock prediction
        """
        message = (
            f"🚨 iClinic ALERT\n"
            f"Medicine: {medicine_name}\n"
            f"Current Stock: {current_stock}\n"
            f"AI Prediction: Will run out in {predicted_days} days\n"
            f"Reorder Point: {reorder_point}\n"
            f"Action: Order new stock immediately!"
        )
        
        return self._send_to_admins(message)
    
    def send_expiry_warning(self, medicine_name: str, batch_number: str, 
                           expiry_date: str, days_until_expiry: int) -> Dict:
        """
        Send SMS alert for expiring medicines
        """
        message = (
            f"⚠️ iClinic EXPIRY WARNING\n"
            f"Medicine: {medicine_name}\n"
            f"Batch: {batch_number}\n"
            f"Expires: {expiry_date}\n"
            f"Days Left: {days_until_expiry}\n"
            f"Action: Use or dispose soon!"
        )
        
        return self._send_to_admins(message)
    
    def send_restock_recommendation(self, medicine_name: str, 
                                   recommended_quantity: int, 
                                   reason: str) -> Dict:
        """
        Send SMS with AI restock recommendation
        """
        message = (
            f"💡 iClinic AI RECOMMENDATION\n"
            f"Medicine: {medicine_name}\n"
            f"Suggested Order: {recommended_quantity} units\n"
            f"Reason: {reason}\n"
            f"AI-powered inventory optimization"
        )
        
        return self._send_to_admins(message)
    
    def send_critical_shortage(self, medicine_name: str, current_stock: int) -> Dict:
        """
        Send URGENT SMS for critical stock shortage
        """
        message = (
            f"🆘 URGENT - iClinic\n"
            f"CRITICAL SHORTAGE!\n"
            f"Medicine: {medicine_name}\n"
            f"Stock: {current_stock} (VERY LOW)\n"
            f"IMMEDIATE ACTION REQUIRED!"
        )
        
        return self._send_to_admins(message)
    
    def send_daily_summary(self, total_medicines: int, low_stock_count: int, 
                          expiring_soon: int) -> Dict:
        """
        Send daily inventory summary SMS
        """
        message = (
            f"📊 iClinic Daily Report\n"
            f"Total Medicines: {total_medicines}\n"
            f"Low Stock Items: {low_stock_count}\n"
            f"Expiring Soon: {expiring_soon}\n"
            f"Date: {datetime.now().strftime('%Y-%m-%d')}"
        )
        
        return self._send_to_admins(message)
    
    def _send_to_admins(self, message: str) -> Dict:
        """
        Send SMS to all configured admin phone numbers
        """
        if not self.admin_phones:
            logger.warning("⚠️ No admin phones configured for SMS notifications")
            return {
                'success': False,
                'error': 'No admin phones configured'
            }
        
        recipients = [
            {'phone': phone, 'message': message}
            for phone in self.admin_phones
        ]
        
        return self.sms.send_bulk_sms(recipients)


# Example usage and testing
if __name__ == "__main__":
    # Test LOCAL (offline) mode
    print("🧪 Testing Android SMS Gateway Integration...\n")
    
    # Initialize gateway in LOCAL mode (works offline)
    gateway = AndroidSMSGateway(use_local=True)
    
    # Check status
    status = gateway.check_status()
    print(f"Gateway Status: {status}\n")
    
    # Test SMS sending
    test_result = gateway.send_sms(
        phone_number="09557850712",  # Replace with your test number
        message="🧪 iClinic Test: Android SMS Gateway is working! This is a FREE SMS sent offline."
    )
    print(f"Test SMS Result: {test_result}\n")
    
    # Test inventory notifier
    notifier = InventorySMSNotifier(gateway)
    notifier.set_admin_phones(["09557850712"])  # Replace with admin numbers
    
    # Test low stock alert
    alert_result = notifier.send_low_stock_alert(
        medicine_name="Paracetamol 500mg",
        current_stock=15,
        predicted_days=3,
        reorder_point=20
    )
    print(f"Low Stock Alert Result: {alert_result}")

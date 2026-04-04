import os


class SMSConfig:
    # Set to 'semaphore' to use Semaphore SMS API
    SMS_PROVIDER = (os.environ.get('SMS_PROVIDER') or 'android_gateway').strip()

    ANDROID_SMS_GATEWAY_MODE = (os.environ.get('ANDROID_SMS_GATEWAY_MODE') or 'local').strip()
    ANDROID_SMS_GATEWAY_LOCAL_BASE_URL = (os.environ.get('ANDROID_SMS_GATEWAY_LOCAL_BASE_URL') or 'http://192.168.100.47:8080/').strip()
    ANDROID_SMS_GATEWAY_CLOUD_BASE_URL = (os.environ.get('ANDROID_SMS_GATEWAY_CLOUD_BASE_URL') or 'https://api.sms-gate.app:443').strip()

    ANDROID_SMS_GATEWAY_LOCAL_USERNAME = (os.environ.get('ANDROID_SMS_GATEWAY_LOCAL_USERNAME') or 'sms').strip()
    ANDROID_SMS_GATEWAY_LOCAL_PASSWORD = (os.environ.get('ANDROID_SMS_GATEWAY_LOCAL_PASSWORD') or 'yettB3in').strip()

    ANDROID_SMS_GATEWAY_CLOUD_USERNAME = (os.environ.get('ANDROID_SMS_GATEWAY_CLOUD_USERNAME') or '').strip()
    ANDROID_SMS_GATEWAY_CLOUD_PASSWORD = (os.environ.get('ANDROID_SMS_GATEWAY_CLOUD_PASSWORD') or '').strip()

import os


class SMSConfig:
    SMS_PROVIDER = (os.environ.get('SMS_PROVIDER') or '').strip()

    PHILSMS_API_TOKEN = (os.environ.get('PHILSMS_API_TOKEN') or '').strip()
    PHILSMS_SENDER_ID = (os.environ.get('PHILSMS_SENDER_ID') or '').strip()
    PHILSMS_SMS_TYPE = (os.environ.get('PHILSMS_SMS_TYPE') or '').strip()
    PHILSMS_CONTACT_LIST_ID = (os.environ.get('PHILSMS_CONTACT_LIST_ID') or '').strip()

    SEMAPHORE_API_KEY = (os.environ.get('SEMAPHORE_API_KEY') or '').strip()
    SEMAPHORE_SENDER_NAME = (os.environ.get('SEMAPHORE_SENDER_NAME') or '').strip()

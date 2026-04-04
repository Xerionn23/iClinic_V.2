import os


class SMSConfig:
    # Set to 'semaphore' to use Semaphore SMS API
    SMS_PROVIDER = (os.environ.get('SMS_PROVIDER') or 'semaphore').strip()

    PHILSMS_API_TOKEN = (os.environ.get('PHILSMS_API_TOKEN') or '').strip()
    PHILSMS_SENDER_ID = (os.environ.get('PHILSMS_SENDER_ID') or '').strip()
    PHILSMS_SMS_TYPE = (os.environ.get('PHILSMS_SMS_TYPE') or '').strip()
    PHILSMS_CONTACT_LIST_ID = (os.environ.get('PHILSMS_CONTACT_LIST_ID') or '').strip()
    # SEMAPHORE API KEY - PASTE YOUR KEY HERE
    SEMAPHORE_API_KEY = (os.environ.get('SEMAPHORE_API_KEY') or '3533cf16b93251cfe1d84f6f525b87fc').strip()
    SEMAPHORE_SENDER_NAME = (os.environ.get('SEMAPHORE_SENDER_NAME') or '').strip()

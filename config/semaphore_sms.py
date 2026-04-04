import os


# ============================================
# SEMAPHORE SMS CONFIGURATION
# ============================================
# 
# 1. Get your API key from https://semaphore.co/
# 2. Paste your API key below (replace the placeholder)
# 3. Done! No sender name needed - uses random number by default
#
# NOTE: Leave SEMAPHORE_SENDER_NAME empty to use random number
# If you register a sender name later, add it to the env variable
# ============================================

# PASTE YOUR SEMAPHORE API KEY HERE
SEMAPHORE_API_KEY = '3533cf16b93251cfe1d84f6f525b87fc'

# Optional: Sender name (leave empty for random number)
SEMAPHORE_SENDER_NAME = os.environ.get('SEMAPHORE_SENDER_NAME', '')


class SemaphoreSMSConfig:
    """Simple Semaphore SMS configuration - API key only, no sender name needed"""
    
    @classmethod
    def get_api_key(cls):
        """Get the API key - checks env var first, then falls back to config"""
        env_key = os.environ.get('SEMAPHORE_API_KEY', '').strip()
        if env_key:
            return env_key
        return SEMAPHORE_API_KEY if SEMAPHORE_API_KEY != 'YOUR_API_KEY_HERE' else ''
    
    @classmethod
    def get_sender_name(cls):
        """Get sender name (returns None to use random number)"""
        sender = SEMAPHORE_SENDER_NAME.strip()
        return sender if sender else None
    
    @classmethod
    def is_configured(cls):
        """Check if API key is set"""
        return bool(cls.get_api_key())

import base64, traceback, logging

from cryptography.fernet import Fernet

from django.conf import settings

def encrypt(id):
    try:
        id = str(id)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        encrypted_text = cipher_suite.encrypt(id.encode('ascii'))
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode('ascii')

        return encrypted_text

    except:
        logging.getLogger('error_logger').error(traceback.format_exc())
        return None

def decrypt(id):
    try:
        id = base64.urlsafe_b64decode(id)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(id).decode('ascii')
        return decoded_text
    
    except:
        logging.getLogger('error_logger').error(traceback.format_exc())
        return None
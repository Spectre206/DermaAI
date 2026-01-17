import base64
from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_fernet_key():
    """
    Derives a 32-byte URL-safe base64-encoded key from the project SECRET_KEY.
    This ensures we always have a valid key for Fernet without extra config.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'derma_ai_static_salt', # In production, this should be random
        iterations=100000,
    )
    # Generate key from the Django SECRET_KEY
    key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode()))
    return key

class EncryptedTextField(models.TextField):
    """
    A custom Django field that encrypts data before saving to DB
    and decrypts it when loading from DB.
    """
    description = "Text encrypted with Fernet (AES)"

    def __init__(self, *args, **kwargs):
        self.fernet = Fernet(get_fernet_key())
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        """Encrypts data before sending to Database"""
        if not value:
            return value
        # If it's already bytes, assume it's encrypted (edge case), else encrypt
        if isinstance(value, str):
            encrypted_data = self.fernet.encrypt(value.encode('utf-8'))
            return encrypted_data.decode('utf-8') # Store as string in DB
        return value

    def from_db_value(self, value, expression, connection):
        """Decrypts data when loading from Database"""
        if not value:
            return value
        try:
            decrypted_data = self.fernet.decrypt(value.encode('utf-8'))
            return decrypted_data.decode('utf-8')
        except Exception:
            # If decryption fails (e.g. data wasn't encrypted), return raw
            return value
            
    def to_python(self, value):
        """Handles data coming from forms or other Python sources"""
        if not value:
            return value
        # Standard behavior
        return super().to_python(value)
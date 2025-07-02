from cryptography.fernet import Fernet
import hashlib
import os

# ---------------------
# Encryption for File IDs
# ---------------------

# Use a consistent and secure Fernet key across all modules
# You can export this key as an environment variable or hard-code for testing only
# NOTE: DO NOT hardcode keys in production!
SECRET_KEY = os.getenv("FERNET_SECRET", b't2gLjhsmvSQIPgvRojoeohWKH9FCvPKtEmkdkwM4R1w=')
fernet = Fernet(SECRET_KEY)

def generate_encrypted_file_token(file_id: str) -> str:
    """Encrypts file_id to a secure token."""
    return fernet.encrypt(file_id.encode()).decode()

def decrypt_file_token(token: str) -> str:
    """Decrypts secure token back to file_id."""
    return fernet.decrypt(token.encode()).decode()

# ---------------------
# Password Hashing (Not reversible)
# ---------------------

def hash_password(password: str) -> str:
    """Returns SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()

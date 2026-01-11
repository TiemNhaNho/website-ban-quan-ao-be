from datetime import datetime, timedelta
import hashlib
import base64

import bcrypt
import jwt as pyjwt  # Import as pyjwt to avoid conflicts

from app.core.config import get_settings
from app.models.customer_model import Customer

ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = get_settings()

def _preprocess_password(password: str) -> bytes:
    """
    Preprocess password using SHA256 before bcrypt hashing.
    This solves the bcrypt 72-byte limitation.
    Returns bytes ready for bcrypt.
    """
    # Hash password with SHA256 first
    sha256_hash = hashlib.sha256(password.encode('utf-8')).digest()
    # Encode to base64 for safe string representation
    return base64.b64encode(sha256_hash)

def hash_password(password: str) -> str:
    """
    Hash password using SHA256 + bcrypt for maximum security.
    Handles passwords of any length.
    Uses bcrypt directly instead of passlib to avoid version detection issues.
    """
    preprocessed = _preprocess_password(password)
    # Use bcrypt directly
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(preprocessed, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str = "") -> bool:
    """
    Verify password against hashed password.
    Supports both old (direct bcrypt) and new (SHA256 + bcrypt) methods.
    Uses bcrypt directly instead of passlib.
    """
    if not hashed_password:
        return False
    
    try:
        # Try new method first (SHA256 + bcrypt)
        preprocessed = _preprocess_password(password)
        if bcrypt.checkpw(preprocessed, hashed_password.encode('utf-8')):
            return True
    except Exception:
        pass
    
    try:
        # Fallback to old method (direct bcrypt) for backward compatibility
        password_bytes = password.encode('utf-8')
        # Truncate to 72 bytes if needed
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        if bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8')):
            return True
    except Exception:
        pass
    
    return False

def create_access_token(customer: Customer) -> str:
    issued_at = datetime.now()
    expired = issued_at + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(customer.id),
        "role": customer.role,
        "iat": int(issued_at.timestamp()),
        "exp": int(expired.timestamp())
    }
    
    token = pyjwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
    return token

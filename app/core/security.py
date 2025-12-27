from datetime import datetime, timedelta

from passlib.context import CryptContext
import jwt

from app.core.config import get_settings
from app.models.customer_model import Customer

ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str = "") -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(customer: Customer) -> str:
    issued_at = datetime.now()
    expired = issued_at + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(customer.id),
        "role": customer.role,
        "iat": int(issued_at.timestamp()),
        "exp": int(expired.timestamp())
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
    return token

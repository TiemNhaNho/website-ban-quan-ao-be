from pydantic import ValidationError

import jwt as pyjwt  # Import as pyjwt to avoid conflicts
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.base import get_db
from app.schemas.customer_schema import TokenPayload
from app.models.customer_model import Customer

reusable_oauth = HTTPBearer(
    scheme_name='Authorization'
)

settings = get_settings()

def authenticate(http_authorization_credentials=Depends(reusable_oauth), db: Session = Depends(get_db)):
    try:
        payload = pyjwt.decode(
            http_authorization_credentials.credentials, settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)

    except (pyjwt.PyJWTError, ValidationError) as e:
        raise HTTPException(
            status_code=403,
            detail="Invalid or expired authentication token"
        )
    customer = db.query(Customer).filter(Customer.id == int(token_data.sub)).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer
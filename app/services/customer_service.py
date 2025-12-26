from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.models.customer_model import Customer

def check_email_exists(email: str, db: Session) -> bool:
    return db.query(exists().where(Customer.email == email)).scalar()
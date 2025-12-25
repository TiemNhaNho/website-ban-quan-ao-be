from fastapi import APIRouter
from app.schemas.customer_schema import RegisterCustomerSchema, CustomerSchema
from app.models.customer_model import Customer
from app.db.base import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.base_schema import DataResponse
from app.core.security import hash_password
router = APIRouter()


@router.post("/register", tags=["customers"], description="Register a new customer", response_model=DataResponse[CustomerSchema])
async def register_user(data: RegisterCustomerSchema, db: Session = Depends(get_db)):
    password = hash_password(data.password)
    user = Customer(username=data.username, email=data.email, password_hash=password)
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return DataResponse.custom_response(code="201", message="Register user success", data=user)
    except Exception as e:
        return DataResponse.custom_response(code="500", message="Register user failed", data=None)



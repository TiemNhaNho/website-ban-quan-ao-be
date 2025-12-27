from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.middleware.authenticate import authenticate
from app.schemas.customer_schema import LoginCustomerResponseSchema, LoginCustomerSchema, RegisterCustomerSchema, CustomerSchema
from app.models.customer_model import Customer
from app.db.base import get_db
from app.schemas.base_schema import DataResponse
from app.core.security import create_access_token, hash_password, verify_password
from app.services.customer_service import check_email_exists

router = APIRouter()


@router.post("/register", tags=["customers"], description="Register a new customer", response_model=DataResponse[CustomerSchema])
async def register_customer(data: RegisterCustomerSchema, db: Session = Depends(get_db)):
    if check_email_exists(data.email, db):
        return DataResponse.custom_response(code="400", message="Email already exists", data=None)
    
    password = hash_password(data.password)
    customer = Customer(username=data.username, email=data.email, password_hash=password)
    try:
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return DataResponse.custom_response(code="201", message="Register new customer successfully", data=customer)
    except Exception as e:
        return DataResponse.custom_response(code="500", message="Register new customer failed", data=None)


@router.post("/login", tags=["customers"], description="Login a customer", response_model=DataResponse[LoginCustomerResponseSchema])
async def login_customer(data: LoginCustomerSchema, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email == data.email).first()
    if not customer or not verify_password(data.password, customer.password_hash):
        return DataResponse.custom_response(code="401", message="Invalid email or password", data=None)
    
    token = create_access_token(customer)
    
    return DataResponse.custom_response(code="200", message="Login customer success", data=LoginCustomerResponseSchema(access_token=token, token_type="Bearer"))

@router.get("/me", tags=["customers"], description="Get current customer", response_model=DataResponse[CustomerSchema], dependencies=[Depends(authenticate)])
async def get_current_customer(current_customer: Customer = Depends(authenticate)):
    return DataResponse.custom_response(code="200", message="Get current customer successfully", data=current_customer)

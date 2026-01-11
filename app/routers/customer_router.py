from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.middleware.authenticate import authenticate
from app.schemas.customer_schema import LoginCustomerResponseSchema, LoginCustomerSchema, RegisterCustomerSchema, CustomerSchema, UpdateCustomerSchema
from app.models.customer_model import Customer
from app.db.base import get_db
from app.schemas.base_schema import DataResponse
from app.core.security import create_access_token, verify_password
from app.services.customer_service import login_with_auth_callback, login_with_google, register_customer_service, login_with_facebook, update_customer_service, deactivate_customer_service

router = APIRouter()

@router.post("/register", tags=["customers"], description="Register a new customer", response_model=DataResponse[CustomerSchema])
def register_customer(data: RegisterCustomerSchema, db: Session = Depends(get_db)):
    return register_customer_service(data, db)
    

@router.get("/activate-account", tags=["customers"], description="Activate a customer account", response_model=DataResponse[LoginCustomerResponseSchema])
def activate_customer_account(emailAddress: str, id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email == emailAddress, Customer.id == id).first()
    if not customer:
        return DataResponse.custom_response(code="404", message="Customer not found", data=None)
    
    if customer.is_deactivated:
        customer.is_deactivated = False
        db.commit()
        db.refresh(customer)
        token = create_access_token(customer)
        return DataResponse.custom_response(code="200", message="Customer account activated successfully", data=LoginCustomerResponseSchema(access_token=token, token_type="Bearer"))
    else:
        return DataResponse.custom_response(code="400", message="Customer account is already active", data=None)

@router.post("/login", tags=["customers"], description="Login a customer", response_model=DataResponse[LoginCustomerResponseSchema])
def login_customer(data: LoginCustomerSchema, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email == data.email).first()
    if not customer or not verify_password(data.password, customer.password_hash):
        return DataResponse.custom_response(code="401", message="Invalid email or password", data=None)
    
    # Kiểm tra tài khoản có bị deactivate không
    if customer.is_deactivated:
        return DataResponse.custom_response(
            code="403", 
            message="Your account has been deactivated. Please contact support or activate your account.", 
            data=None
        )
    
    # Re-hash password if it's using old method (transparent migration)
    try:
        from app.core.security import _preprocess_password, hash_password
        import bcrypt
        preprocessed = _preprocess_password(data.password)
        
        # If old method works but new doesn't, re-hash
        if not bcrypt.checkpw(preprocessed, customer.password_hash.encode('utf-8')):
            customer.password_hash = hash_password(data.password)
            db.commit()
    except Exception:
        pass
    
    token = create_access_token(customer)
    
    return DataResponse.custom_response(code="200", message="Login customer successfully", data=LoginCustomerResponseSchema(access_token=token, token_type="Bearer"))

@router.get("/me", tags=["customers"], description="Get current customer", response_model=DataResponse[CustomerSchema], dependencies=[Depends(authenticate)])
def get_current_customer(current_customer: Customer = Depends(authenticate)):
    return DataResponse.custom_response(code="200", message="Get current customer successfully", data=current_customer)

@router.get("/auth/google", description="Initiate Google OAuth login", response_model=DataResponse[LoginCustomerResponseSchema])
def login_google_oauth():
    return login_with_google()

@router.get("/auth/facebook", description="Initiate Facebook OAuth login", response_model=DataResponse[LoginCustomerResponseSchema])
def login_facebook_oauth():
    return login_with_facebook()

@router.get("/auth/callback", description="Handle OAuth callback", response_model=DataResponse[LoginCustomerResponseSchema])
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    return await login_with_auth_callback(request, db)

@router.put("/me", tags=["customers"], description="Update current customer", response_model=DataResponse[CustomerSchema], dependencies=[Depends(authenticate)])
def update_current_customer(data: UpdateCustomerSchema, current_customer: Customer = Depends(authenticate), db: Session = Depends(get_db)):
    return update_customer_service(current_customer.id, data, db)

@router.post("/me/deactivate", tags=["customers"], description="Deactivate current customer account", response_model=DataResponse[CustomerSchema], dependencies=[Depends(authenticate)])
def deactivate_current_customer(current_customer: Customer = Depends(authenticate), db: Session = Depends(get_db)):
    return deactivate_customer_service(current_customer.id, db)
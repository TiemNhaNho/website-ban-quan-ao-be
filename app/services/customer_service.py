from urllib.parse import urlencode

from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, hash_password
from app.core.utils.email import send_email_with_template
from app.core.utils.password import generate_password
from app.core.utils.logger import logger
from app.models.customer_model import Customer
from app.schemas.base_schema import DataResponse
from app.schemas.customer_schema import LoginCustomerResponseSchema, RegisterCustomerSchema, UpdateCustomerSchema

settings = get_settings()

def check_email_exists(email: str, db: Session) -> bool:
    return db.query(exists().where(Customer.email == email)).scalar()

def send_activation_email(customer: Customer) -> None:
    context = {
        "username": f"{customer.username}",
        "email": f"{customer.email}",
        "activation_link": f"{settings.domain}/activate-account?emailAddress={customer.email}&id={customer.id}",
        "domain": settings.domain
    }

    send_email_with_template(
        recipient=f"{customer.email}",
        subject="Kích hoạt tài khoản của bạn để bắt đầu mua sắm!",
        template_name="activation_email/activation_email.html",
        context=context
    )
    
def login_with_google():
    query_params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
        "state": "google"
    }
    url = f"{settings.GOOGLE_AUTH_ENDPOINT}?{urlencode(query_params)}"
    return RedirectResponse(url)

async def login_with_auth_callback(request: Request, db: Session):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    if state == "google":
        return await handle_google_callback(code, db)
    elif state == "facebook":
        return await handle_facebook_callback(code, db)
    else:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

async def handle_google_callback(code: str, db: Session):
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    async with httpx.AsyncClient() as client:
        token_response = await client.post(settings.GOOGLE_TOKEN_ENDPOINT, data=data)
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token from Google")

        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo_response = await client.get(settings.GOOGLE_USERINFO_ENDPOINT, headers=headers)
        userinfo = userinfo_response.json()
        
        return await process_oauth_user(userinfo, db, "Google")

async def handle_facebook_callback(code: str, db: Session):
    params = {
        "client_id": settings.FACEBOOK_CLIENT_ID,
        "client_secret": settings.FACEBOOK_CLIENT_SECRET,
        "redirect_uri": settings.REDIRECT_URI,
        "code": code,
    }
    
    async with httpx.AsyncClient() as client:
        token_response = await client.get(settings.FACEBOOK_TOKEN_ENDPOINT, params=params)
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token from Facebook")

        params = {
            "fields": "id,name,email,picture",
            "access_token": access_token
        }
        userinfo_response = await client.get(settings.FACEBOOK_USERINFO_ENDPOINT, params=params)
        userinfo = userinfo_response.json()
        
        return await process_oauth_user(userinfo, db, "Facebook")

async def process_oauth_user(userinfo: dict, db: Session, provider: str):
    email = userinfo.get("email")
    name = userinfo.get("name")
    
    if not email:
        raise HTTPException(status_code=400, detail=f"Email not found in {provider} account")

    customer = db.query(Customer).filter(Customer.email == email).first()
    if not customer:
        plain_password = generate_password()
        new_customer_data = RegisterCustomerSchema(
            username=name, 
            email=email, 
            password=plain_password
        )
        response = create_new_customer(new_customer_data, db)
        if response and response.code == "201" and response.data: 
            customer = response.data
        else:
            raise HTTPException(status_code=500, detail="Failed to create customer")
    
    # Kiểm tra tài khoản có bị deactivate không
    if customer.is_deactivated:
        raise HTTPException(
            status_code=403, 
            detail="Your account has been deactivated. Please contact support or activate your account."
        )
        
    token = create_access_token(customer)
    
    return RedirectResponse(f"{settings.FRONTEND_URL}?token={token}")
    
def login_with_facebook():
    query_params = {
        "client_id": settings.FACEBOOK_CLIENT_ID,
        "redirect_uri": settings.REDIRECT_URI,
        "state": "facebook",
        "scope": "email,public_profile",
        "response_type": "code",
    }
    url = f"{settings.FACEBOOK_AUTH_ENDPOINT}?{urlencode(query_params)}"
    return RedirectResponse(url)
    
def create_new_customer(data: RegisterCustomerSchema, db: Session) -> DataResponse | None:
    password = hash_password(data.password)
    customer = Customer(username=data.username, email=data.email, password_hash=password)
    try:
        db.add(customer)
        db.commit()
        db.refresh(customer)
        send_activation_email(customer)
        return DataResponse.custom_response(code="201", message="Register new customer successfully", data=customer)
    except Exception as e:
        logger.error(f"Failed to create customer {data.email}: {str(e)}", exc_info=True)  
        db.rollback()  
        return DataResponse.custom_response(code="500", message="Register new customer failed", data=None)
    
def register_customer_service(data: RegisterCustomerSchema, db: Session) -> DataResponse:
    if check_email_exists(data.email, db):
        return DataResponse.custom_response(code="400", message="Email already exists", data=None)
    return create_new_customer(data, db)

def update_customer_service(customer_id: int, data: UpdateCustomerSchema, db: Session) -> DataResponse:
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return DataResponse.custom_response(code="404", message="Customer not found", data=None)
    
    # Check if email is being changed and if it already exists
    if data.email and data.email != customer.email:
        if check_email_exists(data.email, db):
            return DataResponse.custom_response(code="400", message="Email already exists", data=None)
        customer.email = data.email
    
    # Update username if provided
    if data.username:
        customer.username = data.username
    
    # Update password if provided
    if data.password:
        customer.password_hash = hash_password(data.password)
    
    try:
        db.commit()
        db.refresh(customer)
        return DataResponse.custom_response(code="200", message="Update customer successfully", data=customer)
    except Exception as e:
        logger.error(f"Failed to update customer {customer_id}: {str(e)}", exc_info=True)
        db.rollback()
        return DataResponse.custom_response(code="500", message="Update customer failed", data=None)

def deactivate_customer_service(customer_id: int, db: Session) -> DataResponse:
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return DataResponse.custom_response(code="404", message="Customer not found", data=None)
    
    if customer.is_deactivated:
        return DataResponse.custom_response(code="400", message="Customer account is already deactivated", data=None)
    
    customer.is_deactivated = True
    
    try:
        db.commit()
        db.refresh(customer)
        return DataResponse.custom_response(code="200", message="Deactivate customer successfully", data=customer)
    except Exception as e:
        logger.error(f"Failed to deactivate customer {customer_id}: {str(e)}", exc_info=True)
        db.rollback()
        return DataResponse.custom_response(code="500", message="Deactivate customer failed", data=None)

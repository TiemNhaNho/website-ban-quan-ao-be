import os
from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.utils.email import send_email_with_template
from app.models.customer_model import Customer

settings = get_settings()

def check_email_exists(email: str, db: Session) -> bool:
    return db.query(exists().where(Customer.email == email)).scalar()

def send_activation_email(customer: Customer) -> None:
    context = {
    "username": f"{customer.username}",
    "email": f"{customer.email}",
    "activation_link": f"{settings.domain}/activate-account?emailAddress={customer.email}&id={customer.id}"
}

    send_email_with_template(
        recipient=f"{customer.email}",
        subject="Kích hoạt tài khoản của bạn để bắt đầu mua sắm!",
        template_name="activation_email/activation_email.html",
        context=context
    )
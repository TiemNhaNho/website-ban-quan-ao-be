import os
from app.core.utils.email import send_email_with_template
from app.models.customer_model import Customer
from app.core.config import get_settings

settings = get_settings()

def send_order_confirmation_mail(
    customer: Customer,
    order,
    products_bought: list
) -> None:
    context = {
        "customer": customer,
        "order": order,
        "products_bought": products_bought,
        "domain": settings.domain,
    }

    send_email_with_template(
        template_name="order_confirm_template/order_confirmation_mail.html",
        context=context,
        subject="Thư xác nhận đơn đặt hàng đang test mới nhất",
        recipient=customer.email
    )

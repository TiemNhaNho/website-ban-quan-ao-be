import os
from app.core.utils.email import send_email_with_template
from app.models.customer_model import Customer

def send_order_confirmation_mail(customer: Customer, order) -> None:
    context = {
        "customer": customer,
        "order": order
    }
    send_email_with_template(
        template_name="order_confirm_template/order_confirmation_mail.html",
        context=context,
        subject="Thư xác nhận đơn đặt hàng",
        recipient=customer.email
    )
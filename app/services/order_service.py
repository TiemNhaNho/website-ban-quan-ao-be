from decimal import Decimal

from requests import Session
from app.models.order_model import Order
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
    
def update_order_subtotal_(
    order_id: int,
    subtotal: Decimal,
    db:Session
):
    order = db.query(Order).filter(Order.order_id == order_id).first()

    order.subtotal = subtotal
    db.commit()
    db.refresh(order)
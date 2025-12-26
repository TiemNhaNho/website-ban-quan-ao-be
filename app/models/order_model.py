from app.models.base_model import BaseModel
from enum import Enum
from sqlalchemy import DECIMAL, Column, String, Enum as SANum, Integer, ForeignKey
from datetime import datetime

class OrderStatus(str, Enum):
    NEW = "New",
    PROCESSING = "Processing",
    SHIPPED = "Shipped",
    DELIVERED = "Delivered",
    RETURNED = "Returned"

class Order(BaseModel):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    coupon_id = Column(Integer, ForeignKey("coupons.coupon_id"), nullable=True)
    shipping_method_id = Column(Integer, ForeignKey("shipping_methods.shipping_method_id"), nullable=False)
    order_date = Column(String, nullable=False, default=datetime.utcnow)
    subtotal = Column(DECIMAL, nullable=False)
    discount_amount = Column(DECIMAL, nullable=False)
    shipping_fee = Column(DECIMAL, nullable=False)
    total_money = Column(DECIMAL, nullable=False)
    payment_method = Column(String(50), nullable=False)
    order_status = Column(SANum(OrderStatus, name="order_status"), nullable=False)
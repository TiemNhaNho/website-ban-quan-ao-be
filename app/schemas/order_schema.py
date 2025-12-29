from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.order_model import OrderStatus

class OrderSchema(BaseModel):
    order_id: int
    customer_id: int
    coupon_id: Optional[int] = None
    shipping_method_id: int
    order_date: datetime
    subtotal: float
    discount_amount: float
    shipping_fee: float
    total_money: float
    payment_method: str
    order_status: OrderStatus

    class Config:
        from_attributes = True

class CreateOrderSchema(BaseModel):
    customer_id: int
    coupon_id: Optional[int] = None
    shipping_method_id: int
    # order_date: datetime
    # subtotal: float
    # discount_amount: float
    # shipping_fee: float
    # total_money: float
    payment_method: str
    order_status: OrderStatus = OrderStatus.NEW

class UpdateOrderSchema(BaseModel):
    customer_id: Optional[int] = None
    coupon_id: Optional[int] = None
    shipping_method_id: Optional[int] = None
    # order_date: Optional[datetime] = None
    # subtotal: Optional[float] = None
    # discount_amount: Optional[float] = None
    # shipping_fee: Optional[float] = None
    # total_money: Optional[float] = None
    payment_method: Optional[str] = None
    order_status: Optional[OrderStatus] = None
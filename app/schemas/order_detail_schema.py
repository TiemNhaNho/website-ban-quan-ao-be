from pydantic import BaseModel
from typing import Optional

class OrderDetailSchema(BaseModel):
    order_detail_id: int
    order_id: int
    variant_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class CreateOrderDetailSchema(BaseModel):
    order_id: int
    variant_id: int
    # quantity: int
    #unit_price: float

class UpdateOrderDetailSchema(BaseModel):
    order_id: Optional[int] = None
    variant_id: Optional[int] = None
    # quantity: Optional[int] = None
    #unit_price: Optional[float] = None
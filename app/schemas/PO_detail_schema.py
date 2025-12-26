from pydantic import BaseModel
from typing import Optional

class PurchaseOrderDetailSchema(BaseModel):
    detail_id: int
    order_id: int
    variant_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class CreatePurchaseOrderDetailSchema(BaseModel):
    order_id: int
    variant_id: int
    quantity: int
    unit_price: float

class UpdatePurchaseOrderDetailSchema(BaseModel):
    order_id: Optional[int] = None
    variant_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
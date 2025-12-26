from pydantic import BaseModel
from typing import Optional

class PurchaseOrderDetailSchema(BaseModel):
    po_detail_id: int
    purchase_order_id: int
    variant_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class CreatePurchaseOrderDetailSchema(BaseModel):
    purchase_order_id: int
    variant_id: int
    quantity: int
    unit_price: float

class UpdatePurchaseOrderDetailSchema(BaseModel):
    purchase_order_id: Optional[int] = None
    variant_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
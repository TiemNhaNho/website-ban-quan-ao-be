from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.PO_model import PurchaseOrderStatus

class PurchaseOrderSchema(BaseModel):
    purchase_order_id: int
    supplier_id: int
    import_date: datetime
    total_amount: float
    status: PurchaseOrderStatus

    class Config:
        from_attributes = True

class CreatePurchaseOrderSchema(BaseModel):
    supplier_id: int
    import_date: datetime
    total_amount: float
    status: PurchaseOrderStatus = PurchaseOrderStatus.PENDING

class UpdatePurchaseOrderSchema(BaseModel):
    supplier_id: Optional[int] = None
    import_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    status: Optional[PurchaseOrderStatus] = None
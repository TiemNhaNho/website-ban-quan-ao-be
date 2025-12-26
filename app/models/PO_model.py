from app.models.base_model import BaseModel
from enum import Enum
from sqlalchemy import Column, Integer, ForeignKey, Enum as SAEnum, DateTime

class PurchaseOrderStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class PurchaseOrder(BaseModel):
    __tablename__ = "purchase_orders"

    purchase_order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=False)
    import_date = Column(DateTime, )
    total_amount = Column(Integer, nullable=False)
    status = Column(SAEnum(PurchaseOrderStatus, name="purchase_order_status"), nullable=False)
from app.models.base_model import BaseModel
from sqlalchemy import Column, DECIMAL, Integer, ForeignKey

class PurchaseOrderDetail(BaseModel):
    __tablename__ = "purchase_order_details"

    detail_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("purchase_orders.purchase_order_id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("product_variants.variant_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL, nullable=False)
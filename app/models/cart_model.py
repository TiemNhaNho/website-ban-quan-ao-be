from app.models.base_model import BaseModel
from sqlalchemy import Column, String, DECIMAL, Integer, ForeignKey, DateTime
from datetime import datetime

class Cart(BaseModel):
    __tablename__ = "carts"

    cart_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("product_variants.variant_id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Text, Integer, DECIMAL

class ShippingMethod(BaseModel):
    __tablename__ = "shipping_methods"

    shipping_method_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    method_name = Column(String(100), nullable=False)
    base_cost = Column(DECIMAL, nullable=False)
    estimated_days = Column(Integer, nullable=False)
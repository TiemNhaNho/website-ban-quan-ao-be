from unicodedata import decimal
from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, DECIMAL

class ProductVariant(BaseModel):
    __tablename__ = "product_variants"
    variant_id: int = Column(Integer, primary_key=True, index=True)
    product_id: int = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    sku: str = Column(String(10), index=True) 
    size: str = Column(String(50), index=True)
    color: str = Column(String(50), index=True)
    stock_quantity: int = Column(Integer, index=True)
    price_in = Column(DECIMAL, index=True)
    price_out = Column(DECIMAL, index=True)

from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Text, Integer, ForeignKey

# class Product(BaseModel):
#     __tablename__ = "products"
#     id: int = Column(Integer, primary_key=True, index=True)
#     name: str = Column(String, index=True)
#     description: str = Column(String, index=True)
#     price: float = Column(Float, index=True)
#     deleted_at: datetime.datetime = Column(DateTime, index=True, nullable=True)

class Product(BaseModel):
    __tablename__ = "products"
    product_id: int = Column(Integer, primary_key=True, index=True)
    category_id: int = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    product_name: str = Column(String(200), index=True)
    description: str = Column(Text, index=True)
    brand: str = Column(String(100), index=True)
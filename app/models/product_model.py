from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Text, Integer, ForeignKey

class Product(BaseModel):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    product_name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    brand = Column(String(100))
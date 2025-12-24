from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Text, Integer, ForeignKey

class ProductImage(BaseModel):
    __tablename__ = "product_images"
    image_id: int = Column(Integer, primary_key=True, index=True)
    product_id: int = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    image_url: str = Column(Text, index=True)
    is_main: bool = Column(Integer, index=True, default=0)
    sort_order: int = Column(Integer, index=True, default=0)

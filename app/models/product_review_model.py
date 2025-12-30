from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime 
from datetime import datetime

class ProductReview(BaseModel):
    __tablename__ = "product_reviews"
    
    review_id: int = Column(Integer, primary_key=True, index=True)
    product_id: int = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    customer_id: int = Column(Integer, ForeignKey("customers.id"), nullable=False)
    rating: int = Column(Integer, index=True, nullable=False)
    comment: str = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, index=True, default=datetime.utcnow)

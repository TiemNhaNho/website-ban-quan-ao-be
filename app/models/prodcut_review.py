from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime 
from datetime import datetime

class ProductReview(BaseModel):
    __tablename__ = "product_reviews"
    
    review_id: int = Column(Integer, primary_key=True, index=True)
    product_id: int = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rating: int = Column(Integer, index=True)
    comment: str = Column(Text, index=True)
    created_at: datetime.datetime = Column(DateTime, index=True, default=datetime.datetime.utcnow)

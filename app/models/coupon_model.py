from app.models.base_model import BaseModel
from sqlalchemy import Column, String, DECIMAL, Integer, ForeignKey, DateTime
from datetime import datetime

class Coupon(BaseModel):
    __tablename__ = "coupons"

    coupon_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    discount_type = Column(String(50), nullable=False)  # e.g., 'percentage' or 'fixed'
    discount_value = Column(DECIMAL, nullable=False)
    min_order_value = Column(DECIMAL, nullable=True)
    max_discount = Column(DECIMAL, nullable=True)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    usage_limit = Column(Integer, nullable=True)
    used_count = Column(Integer, default=0)
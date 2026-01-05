from app.models.base_model import BaseModel
from enum import Enum
from sqlalchemy import Column, String, DECIMAL, Integer, DateTime, Enum as SAEnum
from datetime import datetime

class CouponType(str, Enum):
    FIXED = "Fixed",
    PERCENTAGE = "Percentage",
    
class Coupon(BaseModel):
    __tablename__ = "coupons"

    coupon_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    discount_type = Column(SAEnum(CouponType, name="coupon_type"), nullable=False)
    discount_value = Column(DECIMAL, nullable=False)
    min_order_value = Column(DECIMAL, nullable=True)
    max_discount = Column(DECIMAL, nullable=True)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    usage_limit = Column(Integer, nullable=True)
    used_count = Column(Integer, default=0)
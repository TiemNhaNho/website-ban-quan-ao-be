from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.coupon_model import CouponType

class CouponSchema(BaseModel):
    coupon_id: int
    code: str
    discount_type: CouponType
    discount_value: float
    min_order_value: float
    max_discount: float
    start_date: datetime
    end_date: datetime
    usage_limit: int
    used_count: int

    class Config:
        from_attributes = True

class CreateCouponSchema(BaseModel):
    code: str
    discount_type: CouponType = CouponType.FIXED
    discount_value: float
    min_order_value: float
    max_discount: float
    start_date: datetime
    end_date: datetime
    usage_limit: int
     
class UpdateCouponSchema(BaseModel):
    code: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    min_order_value: Optional[float] = None
    max_discount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None
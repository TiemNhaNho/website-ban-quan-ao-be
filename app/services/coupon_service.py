from sqlalchemy.orm import Session
from app.models.coupon_model import Coupon
from app.schemas.base_schema import DataResponse


def update_coupon_used_count_(
    coupon_id: int,
    used_count: int,
    db: Session
):
    coupon = db.query(Coupon).filter(Coupon.coupon_id == coupon_id).first()

    coupon.used_count = used_count
    db.commit()
    db.refresh(coupon)


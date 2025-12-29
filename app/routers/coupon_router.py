from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.coupon_model import Coupon
from app.db.base import get_db
from app.schemas.coupon_schema import CouponSchema, CreateCouponSchema, UpdateCouponSchema
from app.schemas.base_schema import DataResponse
from app.services.coupon_service import update_coupon_used_count_

router = APIRouter()

@router.get("/coupons", tags=["coupons"], description="Get all coupons", response_model=DataResponse[list[CouponSchema]])
async def get_coupons(db: Session = Depends(get_db)):
    coupons = db.query(Coupon).all()
    return DataResponse.custom_response(
        code="200", message="Get list coupons", data=coupons
    )

@router.get("/coupons/{coupon_id}", tags=["coupons"], description="Get a coupon by id", response_model=DataResponse[CouponSchema])
async def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(Coupon.coupon_id == coupon_id).first()
    if not coupon:
        return DataResponse.custom_response(
            code="404", message="Coupon not found", data=None
        )
    return DataResponse.custom_response(
        code="200", message="Get coupon by id", data=coupon
    )

@router.post("/coupons", tags=["coupons"], description="Create a new coupon", response_model=DataResponse[CouponSchema])
async def create_coupon(data: CreateCouponSchema, db: Session = Depends(get_db)):
    coupon = Coupon(**data.dict())
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return DataResponse.custom_response(
        code="201", message="Coupon created successfully", data=coupon
    )

@router.put("/coupons/{coupon_id}", tags=["coupons"], description="Update a coupon by id", response_model=DataResponse[CouponSchema])
async def update_coupon(coupon_id: int, data: UpdateCouponSchema, db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(Coupon.coupon_id == coupon_id).first()
    if not coupon:
        return DataResponse.custom_response(
            code="404", message="Coupon not found", data=None
        )
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(coupon, key, value)
    db.commit()
    db.refresh(coupon)
    return DataResponse.custom_response(
        code="200", message="Coupon updated by id", data=coupon
    )

@router.delete("/coupons/{coupon_id}", tags=["coupons"], description="Delete a coupon by id", response_model=DataResponse[None])
async def delete_coupon(coupon_id: int, db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(Coupon.coupon_id == coupon_id).first()
    if not coupon:
        return DataResponse.custom_response(
            code="404", message="Coupon not found", data=None
        )
    db.delete(coupon)
    db.commit()
    return DataResponse.custom_response(
        code="200", message="Coupon deleted by id", data=None
    )

#only update the used_count field
@router.patch("/coupons/{coupon_id}", tags=["coupons"], description="Update coupon used count by id", response_model=DataResponse[CouponSchema])
async def update_coupon_used_count(coupon_id: int, used_count: int, db: Session = Depends(get_db)):
    update_coupon_used_count_(coupon_id, used_count, db)
    return DataResponse.custom_response(
        code="200",
        message="Coupon usage count updated successfully",
        data=db.query(Coupon).filter(Coupon.coupon_id == coupon_id).first()
    )

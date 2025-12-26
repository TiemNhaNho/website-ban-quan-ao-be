from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.shipping_method_model import ShippingMethod
from app.db.base import get_db
from app.schemas.shipping_method_schema import ShippingMethodSchema, CreateShippingMethodSchema, UpdateShippingMethodSchema
from app.schemas.base_schema import DataResponse

router = APIRouter()

@router.get("/shipping-methods", tags=["shipping-methods"], description="Get all shipping methods", response_model=DataResponse[list[ShippingMethodSchema]])
async def get_shipping_methods(db: Session = Depends(get_db)):
    shipping_methods = db.query(ShippingMethod).all()
    return DataResponse.custom_response(
        code="200", message="Get list shipping methods", data=shipping_methods
    )

@router.get("/shipping-methods/{shipping_method_id}", tags=["shipping-methods"], description="Get a shipping method by id", response_model=DataResponse[ShippingMethodSchema])
async def get_shipping_method(shipping_method_id: int, db: Session = Depends(get_db)):
    shipping_method = db.query(ShippingMethod).filter(ShippingMethod.shipping_method_id == shipping_method_id).first()
    if not shipping_method:
        return DataResponse.custom_response(
            code="404", message="Shipping method not found", data=None
        )
    return DataResponse.custom_response(
        code="200", message="Get shipping method by id", data=shipping_method
    )

@router.post("/shipping-methods", tags=["shipping-methods"], description="Create a new shipping method", response_model=DataResponse[ShippingMethodSchema])
async def create_shipping_method(data: CreateShippingMethodSchema, db: Session = Depends(get_db)):
    shipping_method = ShippingMethod(**data.dict())
    db.add(shipping_method)
    db.commit()
    db.refresh(shipping_method)
    return DataResponse.custom_response(
        code="201", message="Shipping method created successfully", data=shipping_method
    )

@router.put("/shipping-methods/{shipping_method_id}", tags=["shipping-methods"], description="Update a shipping method by id", response_model=DataResponse[ShippingMethodSchema])
async def update_shipping_method(shipping_method_id: int, data: UpdateShippingMethodSchema, db: Session = Depends(get_db)):
    shipping_method = db.query(ShippingMethod).filter(ShippingMethod.shipping_method_id == shipping_method_id).first()
    if not shipping_method:
        return DataResponse.custom_response(
            code="404", message="Shipping method not found", data=None
        )
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(shipping_method, key, value)
    db.commit()
    db.refresh(shipping_method)
    return DataResponse.custom_response(
        code="200", message="Shipping method updated by id", data=shipping_method
    )

@router.delete("/shipping-methods/{shipping_method_id}", tags=["shipping-methods"], description="Delete a shipping method by id", response_model=DataResponse[None])
async def delete_shipping_method(shipping_method_id: int, db: Session = Depends(get_db)):
    shipping_method = db.query(ShippingMethod).filter(ShippingMethod.shipping_method_id == shipping_method_id).first()
    if not shipping_method:
        return DataResponse.custom_response(
            code="404", message="Shipping method not found", data=None
        )
    db.delete(shipping_method)
    db.commit()
    return DataResponse.custom_response(
        code="200", message="Shipping method deleted by id", data=None
    )

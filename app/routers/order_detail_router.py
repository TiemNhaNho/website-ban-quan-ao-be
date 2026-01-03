from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.order_detail_model import OrderDetail
from app.schemas.order_detail_schema import OrderDetailSchema, CreateOrderDetailSchema, UpdateOrderDetailSchema
from app.schemas.base_schema import DataResponse
from app.models.product_variant import ProductVariant

router = APIRouter()

@router.get("/order-details", tags=["order-details"], description="Get all order details", response_model=DataResponse[list[OrderDetailSchema]])
async def get_order_details(db: Session = Depends(get_db)):
	details = db.query(OrderDetail).all()
	return DataResponse.custom_response(code="200", message="Get list of order details", data=details)

@router.post("/order-details", tags=["order-details"], description="Create a new order detail", response_model=DataResponse[OrderDetailSchema])
async def create_order_detail(data: CreateOrderDetailSchema, db: Session = Depends(get_db)):
	unit = db.query(ProductVariant).filter(ProductVariant.variant_id == data.variant_id).first()
	unit_price = unit.price_out if unit else 0
	db_detail = OrderDetail(
		order_id=data.order_id,
		variant_id=data.variant_id,
		unit_price=unit_price
	)
	db.add(db_detail)
	db.commit()
	db.refresh(db_detail)
	return DataResponse.custom_response(code="201", message="Created order detail", data=db_detail)

@router.get("/order-details/{order_detail_id}", tags=["order-details"], description="Get an order detail by id", response_model=DataResponse[OrderDetailSchema])
async def get_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
	detail = db.query(OrderDetail).filter(OrderDetail.order_detail_id == order_detail_id).first()
	if not detail:
		return DataResponse.custom_response(code="404", message="Order detail not found", data=None)
	return DataResponse.custom_response(code="200", message="Get order detail by id", data=detail)

@router.delete("/order-details/{order_detail_id}", tags=["order-details"], description="Delete an order detail by id", response_model=DataResponse[OrderDetailSchema])
async def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
	detail = db.query(OrderDetail).filter(OrderDetail.order_detail_id == order_detail_id).first()
	if not detail:
		return DataResponse.custom_response(code="404", message="Order detail not found", data=None)
	db.delete(detail)
	db.commit()
	return DataResponse.custom_response(code="200", message="Deleted order detail", data=None)

@router.put("/order-details/{order_detail_id}", tags=["order-details"], description="Update an order detail by id", response_model=DataResponse[OrderDetailSchema])
async def update_order_detail(order_detail_id: int, data: UpdateOrderDetailSchema, db: Session = Depends(get_db)):
	detail = db.query(OrderDetail).filter(OrderDetail.order_detail_id == order_detail_id).first()
	if not detail:
		return DataResponse.custom_response(code="404", message="Order detail not found", data=None)
	update_data = data.dict(exclude_unset=True)
	for key, value in update_data.items():
		setattr(detail, key, value)
	db.commit()
	db.refresh(detail)
	return DataResponse.custom_response(code="200", message="Updated order detail", data=detail)

#only update the quantity
@router.patch("/order-details/{order_detail_id}", tags=["order-details"], description="Update quantity of an order detail", response_model=DataResponse[OrderDetailSchema])
async def update_order_detail_quantity(order_detail_id: int, quantity: int, db: Session = Depends(get_db)):
    order_detail = db.query(OrderDetail).filter(OrderDetail.order_detail_id == order_detail_id).first()
    if not order_detail:
        return DataResponse.custom_response(
            code="404", message="Order detail not found", data=None
        )
    order_detail.quantity = quantity
    db.commit()
    db.refresh(order_detail)
    return DataResponse.custom_response(
        code="200", message="Order detail quantity updated successfully", data=order_detail
    )
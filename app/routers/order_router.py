from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.order_model import Order
from app.models.shipping_method_model import ShippingMethod
from app.models.coupon_model import Coupon
from app.schemas.order_schema import OrderSchema, CreateOrderDetailSchema, UpdateOrderDetailSchema
from app.schemas.base_schema import DataResponse
from utils import get_customer_options

router = APIRouter()

@router.get("/orders", tags=["orders"], description="Get all orders", response_model=DataResponse[list[OrderSchema]])
async def get_orders(db: Session = Depends(get_db)):
	orders = db.query(Order).all()
	return DataResponse.custom_response(code="200", message="Get list of orders", data=orders)

@router.post("/orders", tags=["orders"], description="Create a new order", response_model=DataResponse[OrderSchema])
async def create_order(data: CreateOrderDetailSchema, db: Session = Depends(get_db)):
	db_order = Order(**data.dict())
	db.add(db_order)
	db.commit()
	db.refresh(db_order)
	return DataResponse.custom_response(code="201", message="Created order", data=db_order)

@router.get("/orders/{order_id}", tags=["orders"], description="Get an order by id", response_model=DataResponse[OrderSchema])
async def get_order(order_id: int, db: Session = Depends(get_db)):
	order = db.query(Order).filter(Order.id == order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Order not found", data=None)
	return DataResponse.custom_response(code="200", message="Get order by id", data=order)

@router.delete("/orders/{order_id}", tags=["orders"], description="Delete an order by id", response_model=DataResponse[OrderSchema])
async def delete_order(order_id: int, db: Session = Depends(get_db)):
	order = db.query(Order).filter(Order.id == order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Order not found", data=None)
	db.delete(order)
	db.commit()
	return DataResponse.custom_response(code="200", message="Deleted order", data=None)

@router.put("/orders/{order_id}", tags=["orders"], description="Update an order by id", response_model=DataResponse[OrderSchema])
async def update_order(order_id: int, data: UpdateOrderDetailSchema, db: Session = Depends(get_db)):
	order = db.query(Order).filter(Order.id == order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Order not found", data=None)
	update_data = data.dict(exclude_unset=True)
	for key, value in update_data.items():
		setattr(order, key, value)
	db.commit()
	db.refresh(order)
	return DataResponse.custom_response(code="200", message="Updated order", data=order)

# Get customer options to dropdown input for order creation
@router.get("/customers/options", tags=["orders"], description="Get customer options for order creation")
def customer_options(db:Session = Depends(get_db)):
    return get_customer_options(db)

# Get coupon options to dropdown input for order creation
@router.get("/coupons/options", tags=["orders"], description="Get coupon options for order creation")
def coupon_options(db:Session = Depends(get_db)):
    return db.query(Coupon.coupon_id, Coupon.code).all()

# Get shipping method options to dropdown input for order creation
@router.get("/shipping-methods/options", tags=["orders"], description="Get shipping method options for order creation")
def shipping_method_options(db:Session = Depends(get_db)):
    return db.query(ShippingMethod.shipping_method_id, ShippingMethod.name).all()
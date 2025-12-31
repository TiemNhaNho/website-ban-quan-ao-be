from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.customer_model import Customer
from app.models.order_model import Order
from app.schemas.order_schema import OrderSchema, CreateOrderDetailSchema, UpdateOrderDetailSchema
from app.schemas.base_schema import DataResponse
from app.services.order_service import send_order_confirmation_mail
from app.models.shipping_method_model import ShippingMethod
from app.models.coupon_model import Coupon

router = APIRouter()

@router.get("/orders", tags=["orders"], description="Get all orders", response_model=DataResponse[list[OrderSchema]])
async def get_orders(db: Session = Depends(get_db)):
	orders = db.query(Order).all()
	return DataResponse.custom_response(code="200", message="Get list of orders", data=orders)

@router.post("/orders", tags=["orders"], description="Create a new order", response_model=DataResponse[OrderSchema])
async def create_order(data: CreateOrderDetailSchema, db: Session = Depends(get_db)):
	shipping = db.query(ShippingMethod).filter(ShippingMethod.shipping_method_id == data.shipping_method_id).first()
	coupon = db.query(Coupon).filter(Coupon.coupon_id == data.coupon_id).first()
	discount_amount = coupon.discount_value if coupon else 0
	shipping_fee = shipping.base_cost
	db_order = Order(
		customer_id=data.customer_id,
		coupon_id=data.coupon_id,
		shipping_method_id=data.shipping_method_id,
		discount_amount=discount_amount,
		shipping_fee=shipping_fee,
		payment_method=data.payment_method,
	)
	db.add(db_order)
	db.commit()
	db.refresh(db_order)
	customer = db.query(Customer).filter(Customer.id == db_order.customer_id).first()
	if customer:
		send_order_confirmation_mail(customer, db_order)
	return DataResponse.custom_response(code="201", message="Created order", data=db_order)

@router.get("/orders/{order_id}", tags=["orders"], description="Get an order by id", response_model=DataResponse[OrderSchema])
async def get_order(order_id: int, db: Session = Depends(get_db)):
	order = db.query(Order).filter(Order.order_id == order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Order not found", data=None)
	return DataResponse.custom_response(code="200", message="Get order by id", data=order)

@router.delete("/orders/{order_id}", tags=["orders"], description="Delete an order by id", response_model=DataResponse[OrderSchema])
async def delete_order(order_id: int, db: Session = Depends(get_db)):
	order = db.query(Order).filter(Order.order_id == order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Order not found", data=None)
	db.delete(order)
	db.commit()
	return DataResponse.custom_response(code="200", message="Deleted order", data=None)

@router.put("/orders/{order_id}", tags=["orders"], description="Update an order by id", response_model=DataResponse[OrderSchema])
async def update_order(order_id: int, data: UpdateOrderDetailSchema, db: Session = Depends(get_db)):
	order = db.query(Order).filter(Order.order_id == order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Order not found", data=None)
	update_data = data.dict(exclude_unset=True)
	for key, value in update_data.items():
		setattr(order, key, value)
	db.commit()
	db.refresh(order)
	return DataResponse.custom_response(code="200", message="Updated order", data=order)

#only updade order_status
@router.patch("/orders/{order_id}", tags=["orders"], description="Update order status by id", response_model=DataResponse[OrderSchema])
async def update_order_status(order_id: int, order_status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return DataResponse.custom_response(code="404", message="Order not found", data=None)
    order.order_status = order_status
    db.commit()
    db.refresh(order)
    return DataResponse.custom_response(code="200", message="Updated order status", data=order)
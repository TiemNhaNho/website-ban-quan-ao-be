from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.customer_model import Customer
from app.models.order_model import Order
from app.models.coupon_model import Coupon
from app.models.shipping_method_model import ShippingMethod
from app.models.order_detail_model import OrderDetail
from app.schemas.order_schema import OrderSchema, CreateOrderDetailSchema, UpdateOrderDetailSchema
from app.schemas.base_schema import DataResponse
from app.services.coupon_service import update_coupon_used_count_
from app.services.order_service import send_order_confirmation_mail

router = APIRouter()

@router.get("/orders", tags=["orders"], description="Get all orders", response_model=DataResponse[list[OrderSchema]])
async def get_orders(db: Session = Depends(get_db)):
	orders = db.query(Order).all()
	return DataResponse.custom_response(code="200", message="Get list of orders", data=orders)

@router.post("/orders", tags=["orders"], description="Create a new order", response_model=DataResponse[OrderSchema])
async def create_order(data: CreateOrderDetailSchema, db: Session = Depends(get_db)):
	#Get shipping fee from shipping method
	shipping_method = db.query(ShippingMethod).filter(ShippingMethod.id == data.shipping_method_id).first()
	if not shipping_method:
		return DataResponse.custom_response(code="401", message="Shipping method not found", data=None)
	#Get all item with same order_id from order_detail
	order_details = db.query(OrderDetail).filter(OrderDetail.order_id == Order.order_id).all()
	subtotal = sum([item.quantity * item.unit_price for item in order_details])
	#Get the discount
	discount_amount = 0.0
	if data.coupon_id:
		coupon = db.query(Coupon).filter(Coupon.coupon_id == data.coupon_id).first()
		if coupon:
			if coupon.discount_type == "fixed":
				discount_amount = coupon.discount_value
			discount_amount = subtotal * (coupon.discount_value / 100)
			#Update coupon used count
			update_coupon_used_count_(coupon.coupon_id, coupon.used_count + 1, db)

	#Get shipping fee
	shipping_fee = shipping_method.base_cost
	
	#Total
	total_money = subtotal - discount_amount + shipping_fee

	#Create final order
	db_order = Order(
        customer_id=data.customer_id,
        coupon_id=data.coupon_id,
        shipping_method_id=data.shipping_method_id,
        subtotal=subtotal,
        discount_amount=discount_amount,
        shipping_fee=shipping_fee,
        total_money=total_money,
        payment_method=data.payment_method,
        order_status=data.order_status
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
	#reduce coupon used count when order deleted
	if order.coupon_id:
		coupon = db.query(Coupon).filter(Coupon.coupon_id == order.coupon_id).first()
		if coupon and coupon.used_count > 0:
			update_coupon_used_count_(coupon.coupon_id, coupon.used_count - 1, db)
	db.delete(order)
	db.commit()
	return DataResponse.custom_response(code="200", message="Deleted order", data=None)

@router.put("/orders/{order_id}", tags=["orders"], description="Update an order by id", response_model=DataResponse[OrderSchema])
async def update_order(order_id: int, data: UpdateOrderDetailSchema, db: Session = Depends(get_db)):
	order = db.query(Order).filter(Order.order_id == order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Order not found", data=None)

	# Update fields from input
	update_data = data.dict(exclude_unset=True)
	for key, value in update_data.items():
		setattr(order, key, value)

	# Recalculate subtotal, discount, shipping, total
	shipping_method = db.query(ShippingMethod).filter(ShippingMethod.id == order.shipping_method_id).first()
	if not shipping_method:
		return DataResponse.custom_response(code="401", message="Shipping method not found", data=None)

	order_details = db.query(OrderDetail).filter(OrderDetail.order_id == order.order_id).all()
	subtotal = sum([item.quantity * item.unit_price for item in order_details])

	discount_amount = 0.0
	if order.coupon_id:
		coupon = db.query(Coupon).filter(Coupon.coupon_id == order.coupon_id).first()
		if coupon:
			if coupon.discount_type == "fixed":
				discount_amount = coupon.discount_value
			else:
				discount_amount = subtotal * (coupon.discount_value / 100)
			update_coupon_used_count_(coupon.coupon_id, coupon.used_count + 1, db)

	shipping_fee = shipping_method.base_cost
	total_money = subtotal - discount_amount + shipping_fee

	order.subtotal = subtotal
	order.discount_amount = discount_amount
	order.shipping_fee = shipping_fee
	order.total_money = total_money

	db.commit()
	db.refresh(order)
	return DataResponse.custom_response(code="200", message="Updated order", data=order)

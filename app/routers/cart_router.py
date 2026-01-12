from fastapi import APIRouter, Depends, Query
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.cart_model import Cart
from app.schemas.cart_schema import CartSchema, CreateCartSchema, UpdateCartSchema
from app.schemas.base_schema import DataResponse
from app.models.product_variant import ProductVariant

router = APIRouter()

@router.get("/carts", tags=["carts"], description="Get all carts", response_model=DataResponse[list[CartSchema]])
async def get_carts(db: Session = Depends(get_db)):
	carts = db.query(Cart).all()
	return DataResponse.custom_response(code="200", message="Get list of carts", data=carts)

@router.post("/carts", tags=["carts"], description="Create a new cart", response_model=DataResponse[CartSchema])
async def create_cart(data: CreateCartSchema, db: Session = Depends(get_db)):
	order_variant_id = db.query(ProductVariant).filter(ProductVariant.variant_id == data.variant_id).first()
	if not order_variant_id or order_variant_id.stock_quantity < data.quantity:
		return DataResponse.custom_response(code="400", message="Insufficient stock quantity", data=None)
	db_cart = Cart(**data.dict())
	db.add(db_cart)
	db.commit()
	db.refresh(db_cart)
	return DataResponse.custom_response(code="201", message="Created cart", data=db_cart)

@router.get("/carts/{cart_id}", tags=["carts"], description="Get a cart by id", response_model=DataResponse[CartSchema])
async def get_cart(cart_id: int, db: Session = Depends(get_db)):
	cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
	if not cart:
		return DataResponse.custom_response(code="404", message="Cart not found", data=None)
	return DataResponse.custom_response(code="200", message="Get cart by id", data=cart)

@router.get("/carts-by-customer", tags=["carts"], description="Get carts by customer id")
async def get_carts(
    customer_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Cart)

    if customer_id is not None:
        query = query.filter(Cart.customer_id == customer_id)

    carts = query.all()

    return DataResponse.custom_response(
        code="200",
        message="Get carts",
        data=carts
    )

@router.delete("/carts/{cart_id}", tags=["carts"], description="Delete a cart by id", response_model=DataResponse[CartSchema])
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
	cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
	if not cart:
		return DataResponse.custom_response(code="404", message="Cart not found", data=None)
	db.delete(cart)
	db.commit()
	return DataResponse.custom_response(code="200", message="Deleted cart", data=None)

@router.put("/carts/{cart_id}", tags=["carts"], description="Update a cart by id", response_model=DataResponse[CartSchema])
async def update_cart(cart_id: int, data: UpdateCartSchema, db: Session = Depends(get_db)):
	cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
	if not cart:
		return DataResponse.custom_response(code="404", message="Cart not found", data=None)
	order_variant_id = db.query(ProductVariant).filter(ProductVariant.variant_id == data.variant_id).first()
	if not order_variant_id or order_variant_id.stock_quantity < data.quantity:
		return DataResponse.custom_response(code="400", message="Insufficient stock quantity", data=None)

	update_data = data.dict(exclude_unset=True)
	for key, value in update_data.items():
		setattr(cart, key, value)
	db.commit()
	db.refresh(cart)
	return DataResponse.custom_response(code="200", message="Updated cart", data=cart)

#only update quantity
@router.patch("/carts/{cart_id}", tags=["carts"], description="Update quantity of a cart", response_model=DataResponse[CartSchema])
async def update_cart_quantity(cart_id: int, quantity: int, db: Session = Depends(get_db)):
	cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
	if not cart:
		return DataResponse.custom_response(
			code="404", message="Cart not found", data=None
		)
	order_variant_id = db.query(ProductVariant).filter(ProductVariant.variant_id == cart.variant_id).first()
	if not order_variant_id or order_variant_id.stock_quantity < quantity:
		return DataResponse.custom_response(code="400", message="Insufficient stock quantity", data=None)
	cart.quantity = quantity
	db.commit()
	db.refresh(cart)
	return DataResponse.custom_response(
		code="200", message="Cart quantity updated successfully", data=cart
	)

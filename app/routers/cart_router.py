from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.cart_model import Cart
from app.schemas.cart_schema import CartSchema, CreateCartSchema, UpdateCartSchema
from app.schemas.base_schema import DataResponse
from utils import get_product_variant_options, get_customer_options

router = APIRouter()

@router.get("/carts", tags=["carts"], description="Get all carts", response_model=DataResponse[list[CartSchema]])
async def get_carts(db: Session = Depends(get_db)):
	carts = db.query(Cart).all()
	return DataResponse.custom_response(code="200", message="Get list of carts", data=carts)

@router.post("/carts", tags=["carts"], description="Create a new cart", response_model=DataResponse[CartSchema])
async def create_cart(data: CreateCartSchema, db: Session = Depends(get_db)):
	db_cart = Cart(**data.dict())
	db.add(db_cart)
	db.commit()
	db.refresh(db_cart)
	return DataResponse.custom_response(code="201", message="Created cart", data=db_cart)

@router.get("/carts/{cart_id}", tags=["carts"], description="Get a cart by id", response_model=DataResponse[CartSchema])
async def get_cart(cart_id: int, db: Session = Depends(get_db)):
	cart = db.query(Cart).filter(Cart.id == cart_id).first()
	if not cart:
		return DataResponse.custom_response(code="404", message="Cart not found", data=None)
	return DataResponse.custom_response(code="200", message="Get cart by id", data=cart)

@router.delete("/carts/{cart_id}", tags=["carts"], description="Delete a cart by id", response_model=DataResponse[CartSchema])
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
	cart = db.query(Cart).filter(Cart.id == cart_id).first()
	if not cart:
		return DataResponse.custom_response(code="404", message="Cart not found", data=None)
	db.delete(cart)
	db.commit()
	return DataResponse.custom_response(code="200", message="Deleted cart", data=None)

@router.put("/carts/{cart_id}", tags=["carts"], description="Update a cart by id", response_model=DataResponse[CartSchema])
async def update_cart(cart_id: int, data: UpdateCartSchema, db: Session = Depends(get_db)):
	cart = db.query(Cart).filter(Cart.id == cart_id).first()
	if not cart:
		return DataResponse.custom_response(code="404", message="Cart not found", data=None)
	update_data = data.dict(exclude_unset=True)
	for key, value in update_data.items():
		setattr(cart, key, value)
	db.commit()
	db.refresh(cart)
	return DataResponse.custom_response(code="200", message="Updated cart", data=cart)

# Get customer options to dropdown input for cart creation
@router.get("/customers/options", tags=["carts"], description="Get customer options for cart creation")
def customer_options(db:Session = Depends(get_db)):
    return get_customer_options(db)

# Get product variant options to dropdown input for cart creation
@router.get("/product-variants/options", tags=["carts"], description="Get product variant options for cart creation")
def product_variant_options(db:Session = Depends(get_db)):
    return get_product_variant_options(db)
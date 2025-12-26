from pydantic import BaseModel
from typing import Optional
from datetime import datetime
# class Cart(BaseModel):
#     __tablename__ = "carts"

#     cart_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
#     variant_id = Column(Integer, ForeignKey("product_variants.variant_id"), nullable=False)
#     quantity = Column(Integer, nullable=False, default=0)

class CartSchema(BaseModel):
    cart_id: int
    customer_id: int
    variant_id: int
    quantity: int
    
    class Config:
        from_attributes = True

class CreateCartSchema(BaseModel):
    customer_id: int
    variant_id: int
    quantity: int

class UpdateCartSchema(BaseModel):
    customer_id: Optional[int]
    variant_id: Optional[int]
    quantity: Optional[int]
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
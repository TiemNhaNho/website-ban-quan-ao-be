from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShippingMethodSchema(BaseModel):
    shipping_method_id: int
    method_name: str
    based_cost: float
    estimated_days: int
    
    class Config:
        from_attributes = True

class CreateShippingMethodSchema(BaseModel):
    method_name: str
    based_cost: float
    estimated_days: int

class UpdateShippingMethodSchema(BaseModel):
    method_name: Optional[str] = None
    based_cost: Optional[float] = None
    estimated_days: Optional[int] = None
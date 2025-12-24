from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    id: int
    category_id: int
    name: str
    price: float
    description: str
    brand: str

    class Config:
        from_attributes = True

class CreateProductSchema(BaseModel):
    category_id: int
    name: str
    price: float
    description: str
    brand: str

class UpdateProductSchema(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    brand: Optional[str] = None

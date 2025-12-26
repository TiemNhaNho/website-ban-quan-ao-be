from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    product_id: int
    category_id: int
    product_name: str
    description: str
    brand: str

    class Config:
        from_attributes = True

class CreateProductSchema(BaseModel):
    category_id: int
    product_name: str
    description: str
    brand: str

class UpdateProductSchema(BaseModel):
    category_id: Optional[int] = None
    product_name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None

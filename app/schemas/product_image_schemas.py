from pydantic import BaseModel
from typing import Optional

class ProductImageSchema(BaseModel):
    id: int
    product_id: int
    image_url: str
    is_main: bool
    sort_order: int

    class Config:
        from_attributes = True

class CreateProductImageSchema(BaseModel):
    product_id: int
    image_url: str
    is_main: bool
    sort_order: int

class UpdateProductImageSchema(BaseModel):
    product_id: Optional[int] = None
    image_url: Optional[str] = None
    is_main: Optional[bool] = None
    sort_order: Optional[int] = None
from pydantic import BaseModel
from typing import Optional

class ProductVariantSchema(BaseModel):
    variant_id: int
    product_id: int
    sku: str
    size: str
    color: str
    stock_quantity: int
    price_in: float
    price_out: float

class CreateProductVariantSchema(BaseModel):
    product_id: int
    sku: str
    size: str
    color: str
    # stock_quantity: int
    # price_in: float
    price_out: float

class UpdateProductVariantSchema(BaseModel):
    product_id: Optional[int] = None
    sku: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    # stock_quantity: Optional[int] = None
    # price_in: Optional[float] = None
    price_out: Optional[float] = None
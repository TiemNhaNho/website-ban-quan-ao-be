from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductReviewSchema(BaseModel):
    review_id: int
    product_id: int
    user_id: int
    rating: int
    comment: str
    created_at: datetime.datetime

class CreateProductReviewSchema(BaseModel):
    product_id: int
    rating: int
    comment: str

class UpdateProductReviewSchema(BaseModel):
    product_id: Optional[int] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
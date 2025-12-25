from pydantic import BaseModel
from typing import Optional

class CategorySchema(BaseModel):
    category_id: int
    category_name: str

    class Config:
        from_attributes = True

class CreateCategorySchema(BaseModel):
    category_name: str

class UpdateCategorySchema(BaseModel):
    category_name: Optional[str] = None

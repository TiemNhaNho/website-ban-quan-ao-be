from pydantic import BaseModel
from typing import Optional

class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CreateCategorySchema(BaseModel):
    name: str

class UpdateCategorySchema(BaseModel):
    name: Optional[str] = None

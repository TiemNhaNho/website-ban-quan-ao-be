from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer

class Category(BaseModel):
    __tablename__ = "categories"
    category_id: int = Column(Integer, primary_key=True, index=True)
    category_name: str = Column(String(200), index=True)

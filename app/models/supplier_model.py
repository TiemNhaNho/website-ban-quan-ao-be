from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, CHAR, Text

class Supplier(BaseModel):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_name = Column(String(200), nullable=False)
    phone = Column(CHAR(10), nullable=True)
    address = Column(Text, nullable=True)
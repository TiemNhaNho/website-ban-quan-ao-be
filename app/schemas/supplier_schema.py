from pydantic import BaseModel
from typing import Optional

class SupplierSchema(BaseModel):
    supplier_id: int
    supplier_name: str
    phone: str
    address: str

    class Config:
        from_attributes = True

class CreateSupplierSchema(BaseModel):
    supplier_name: str
    phone: str
    address: str

class UpdateSupplierSchema(BaseModel):
    supplier_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
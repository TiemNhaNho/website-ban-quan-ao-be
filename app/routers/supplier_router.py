from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.supplier_model import Supplier
from app.db.base import get_db
from app.schemas.supplier_schema import SupplierSchema, CreateSupplierSchema, UpdateSupplierSchema
from app.schemas.base_schema import DataResponse
from app.middleware.authorize import require_admin

router = APIRouter()

@router.get("/suppliers", tags=["suppliers"], description="Get all suppliers", response_model=DataResponse[list[SupplierSchema]], dependencies=[Depends(require_admin)])
async def get_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    return DataResponse.custom_response(
        code="200", message="Get list suppliers", data=suppliers
    )
    
@router.get("/suppliers/{supplier_id}", tags=["suppliers"], description="Get a supplier by id", response_model=DataResponse[SupplierSchema], dependencies=[Depends(require_admin)])
async def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        return DataResponse.custom_response(
            code="404", message="Supplier not found", data=None
        )
    return DataResponse.custom_response(
        code="200", message="Get supplier by id", data=supplier
    )
    
@router.post("/suppliers", tags=["suppliers"], description="Create a new supplier", response_model=DataResponse[SupplierSchema], dependencies=[Depends(require_admin)])
async def create_supplier(data: CreateSupplierSchema, db: Session = Depends(get_db)):
    supplier = Supplier(**data.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return DataResponse.custom_response(
        code="201", message="Supplier created successfully", data=supplier
    )

@router.put("/suppliers/{supplier_id}", tags=["suppliers"], description="Update a supplier by id", response_model=DataResponse[SupplierSchema], dependencies=[Depends(require_admin)])
async def update_supplier(supplier_id: int, data: UpdateSupplierSchema, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        return DataResponse.custom_response(
            code="404", message="Supplier not found", data=None
        )
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return DataResponse.custom_response(
        code="200", message="Supplier updated by id", data=supplier
    )

@router.delete("/suppliers/{supplier_id}", tags=["suppliers"], description="Delete a supplier by id", response_model=DataResponse[None], dependencies=[Depends(require_admin)])
async def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        return DataResponse.custom_response(
            code="404", message="Supplier not found", data=None
        )
    db.delete(supplier)
    db.commit()
    return DataResponse.custom_response(
        code="200", message="Supplier deleted by id", data=None
    )
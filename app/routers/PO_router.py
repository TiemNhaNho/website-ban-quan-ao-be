from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.PO_model import PurchaseOrder
from app.models.supplier_model import Supplier
from app.schemas.PO_schema import PurchaseOrderSchema, CreatePurchaseOrderSchema, UpdatePurchaseOrderSchema
from app.schemas.base_schema import DataResponse

router = APIRouter()

@router.get("/purchase-orders", tags=["purchase_orders"], description="Get all purchase orders", response_model=DataResponse[list[PurchaseOrderSchema]])
async def get_purchase_orders(db: Session = Depends(get_db)):
	orders = db.query(PurchaseOrder).all()
	return DataResponse.custom_response(code="200", message="Get list of purchase orders", data=orders)

@router.post("/purchase-orders", tags=["purchase_orders"], description="Create a new purchase order", response_model=DataResponse[PurchaseOrderSchema])
async def create_purchase_order(data: CreatePurchaseOrderSchema, db: Session = Depends(get_db)):
	db_order = PurchaseOrder(**data.dict())
	db.add(db_order)
	db.commit()
	db.refresh(db_order)
	return DataResponse.custom_response(code="201", message="Created purchase order", data=db_order)

@router.get("/purchase-orders/{order_id}", tags=["purchase_orders"], description="Get a purchase order by id", response_model=DataResponse[PurchaseOrderSchema])
async def get_purchase_order(order_id: int, db: Session = Depends(get_db)):
	order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Purchase order not found", data=None)
	return DataResponse.custom_response(code="200", message="Get purchase order by id", data=order)

@router.delete("/purchase-orders/{order_id}", tags=["purchase_orders"], description="Delete a purchase order by id", response_model=DataResponse[PurchaseOrderSchema])
async def delete_purchase_order(order_id: int, db: Session = Depends(get_db)):
	order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Purchase order not found", data=None)
	db.delete(order)
	db.commit()
	return DataResponse.custom_response(code="200", message="Deleted purchase order", data=None)

@router.put("/purchase-orders/{order_id}", tags=["purchase_orders"], description="Update a purchase order by id", response_model=DataResponse[PurchaseOrderSchema])
async def update_purchase_order(order_id: int, data: UpdatePurchaseOrderSchema, db: Session = Depends(get_db)):
	order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Purchase order not found", data=None)
	update_data = data.dict(exclude_unset=True)
	for key, value in update_data.items():
		setattr(order, key, value)
	db.commit()
	db.refresh(order)
	return DataResponse.custom_response(code="200", message="Updated purchase order", data=order)

# Get supplier options to dropdown input for purchase_order creation
@router.get("/suppliers/options", tags=["purchase_orders"], description="Get supplier options for purchase_order creation")
def supplier_options(db:Session = Depends(get_db)):
    return db.query(Supplier.supplier_id, Supplier.supplier_name).all()
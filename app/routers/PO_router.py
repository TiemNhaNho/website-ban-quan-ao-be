from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.PO_model import PurchaseOrder
from app.schemas.PO_schema import PurchaseOrderSchema, CreatePurchaseOrderSchema, UpdatePurchaseOrderSchema
from app.schemas.base_schema import DataResponse
from app.middleware.authorize import require_admin

router = APIRouter()

@router.get("/purchase-orders", tags=["purchase-orders"], description="Get all purchase orders", response_model=DataResponse[list[PurchaseOrderSchema]], dependencies=[Depends(require_admin)])
async def get_purchase_orders(db: Session = Depends(get_db)):
	orders = db.query(PurchaseOrder).all()
	return DataResponse.custom_response(code="200", message="Get list of purchase orders", data=orders)

@router.post("/purchase-orders", tags=["purchase-orders"], description="Create a new purchase order", response_model=DataResponse[PurchaseOrderSchema], dependencies=[Depends(require_admin)])
async def create_purchase_order(data: CreatePurchaseOrderSchema, db: Session = Depends(get_db)):
	db_order = PurchaseOrder(**data.dict())
	db.add(db_order)
	db.commit()
	db.refresh(db_order)
	return DataResponse.custom_response(code="201", message="Created purchase order", data=db_order)

@router.get("/purchase-orders/{purchase_order_id}", tags=["purchase-orders"], description="Get a purchase order by id", response_model=DataResponse[PurchaseOrderSchema], dependencies=[Depends(require_admin)])
async def get_purchase_order(purchase_order_id: int, db: Session = Depends(get_db)):
	order = db.query(PurchaseOrder).filter(PurchaseOrder.purchase_order_id == purchase_order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Purchase order not found", data=None)
	return DataResponse.custom_response(code="200", message="Get purchase order by id", data=order)

@router.delete("/purchase-orders/{purchase_order_id}", tags=["purchase-orders"], description="Delete a purchase order by id", response_model=DataResponse[PurchaseOrderSchema], dependencies=[Depends(require_admin)])
async def delete_purchase_order(purchase_order_id: int, db: Session = Depends(get_db)):
	order = db.query(PurchaseOrder).filter(PurchaseOrder.purchase_order_id == purchase_order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Purchase order not found", data=None)
	db.delete(order)
	db.commit()
	return DataResponse.custom_response(code="200", message="Deleted purchase order", data=None)

@router.put("/purchase-orders/{purchase_order_id}", tags=["purchase-orders"], description="Update a purchase order by id", response_model=DataResponse[PurchaseOrderSchema], dependencies=[Depends(require_admin)])
async def update_purchase_order(purchase_order_id: int, data: UpdatePurchaseOrderSchema, db: Session = Depends(get_db)):
	order = db.query(PurchaseOrder).filter(PurchaseOrder.purchase_order_id == purchase_order_id).first()
	if not order:
		return DataResponse.custom_response(code="404", message="Purchase order not found", data=None)
	update_data = data.dict(exclude_unset=True)
	for key, value in update_data.items():
		setattr(order, key, value)
	db.commit()
	db.refresh(order)
	return DataResponse.custom_response(code="200", message="Updated purchase order", data=order)

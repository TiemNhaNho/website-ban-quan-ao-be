from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.PO_detail_model import PurchaseOrderDetail
from app.db.base import get_db
from app.schemas.PO_detail_schema import PurchaseOrderDetailSchema, CreatePurchaseOrderDetailSchema, UpdatePurchaseOrderDetailSchema
from app.schemas.base_schema import DataResponse
from app.middleware.authorize import require_admin

router = APIRouter()

@router.get("/purchase-order-details", tags=["purchase-order-details"], description="Get all purchase order details", response_model=DataResponse[list[PurchaseOrderDetailSchema]], dependencies=[Depends(require_admin)])
async def get_purchase_order_details(db: Session = Depends(get_db)):
    purchase_order_details = db.query(PurchaseOrderDetail).all()
    return DataResponse.custom_response(
        code="200", message="Get list purchase order details", data=purchase_order_details
    )

@router.get("/purchase-order-details/{po_detail_id}", tags=["purchase-order-details"], description="Get a purchase order detail by id", response_model=DataResponse[PurchaseOrderDetailSchema], dependencies=[Depends(require_admin)])
async def get_purchase_order_detail(po_detail_id: int, db: Session = Depends(get_db)):
    purchase_order_detail = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.po_detail_id == po_detail_id).first()
    if not purchase_order_detail:
        return DataResponse.custom_response(
            code="404", message="Purchase order detail not found", data=None
        )
    return DataResponse.custom_response(
        code="200", message="Get purchase order detail by id", data=purchase_order_detail
    )

@router.post("/purchase-order-details", tags=["purchase-order-details"], description="Create a new purchase order detail", response_model=DataResponse[PurchaseOrderDetailSchema], dependencies=[Depends(require_admin)])
async def create_purchase_order_detail(data: CreatePurchaseOrderDetailSchema, db: Session = Depends(get_db)):
    purchase_order_detail = PurchaseOrderDetail(**data.dict())
    db.add(purchase_order_detail)
    db.commit()
    db.refresh(purchase_order_detail)
    return DataResponse.custom_response(
        code="201", message="Purchase order detail created successfully", data=purchase_order_detail
    )

@router.put("/purchase-order-details/{po_detail_id}", tags=["purchase-order-details"], description="Update a purchase order detail by id", response_model=DataResponse[PurchaseOrderDetailSchema], dependencies=[Depends(require_admin)])
async def update_purchase_order_detail(po_detail_id: int, data: UpdatePurchaseOrderDetailSchema, db: Session = Depends(get_db)):
    purchase_order_detail = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.po_detail_id == po_detail_id).first()
    if not purchase_order_detail:
        return DataResponse.custom_response(
            code="404", message="Purchase order detail not found", data=None
        )
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(purchase_order_detail, key, value)
    db.commit()
    db.refresh(purchase_order_detail)
    return DataResponse.custom_response(
        code="200", message="Purchase order detail updated by id", data=purchase_order_detail
    )

@router.delete("/purchase-order-details/{po_detail_id}", tags=["purchase-order-details"], description="Delete a purchase order detail by id", response_model=DataResponse[None], dependencies=[Depends(require_admin)])
async def delete_purchase_order_detail(po_detail_id: int, db: Session = Depends(get_db)):
    purchase_order_detail = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.po_detail_id == po_detail_id).first()
    if not purchase_order_detail:
        return DataResponse.custom_response(
            code="404", message="Purchase order detail not found", data=None
        )
    db.delete(purchase_order_detail)
    db.commit()
    return DataResponse.custom_response(
        code="200", message="Purchase order detail deleted by id", data=None
    )

#only update the quantity
@router.patch("/purchase-order-details/{po_detail_id}", tags=["purchase-order-details"], description="Update quantity of a purchase order detail", response_model=DataResponse[PurchaseOrderDetailSchema], dependencies=[Depends(require_admin)])
async def update_purchase_order_detail_quantity(po_detail_id: int, quantity: int, db: Session = Depends(get_db)):
    purchase_order_detail = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.po_detail_id == po_detail_id).first()
    if not purchase_order_detail:
        return DataResponse.custom_response(
            code="404", message="Purchase order detail not found", data=None
        )
    purchase_order_detail.quantity = quantity
    db.commit()
    db.refresh(purchase_order_detail)
    return DataResponse.custom_response(
        code="200", message="Purchase order detail quantity updated successfully", data=purchase_order_detail
    )
    

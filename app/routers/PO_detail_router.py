from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.PO_detail_model import PurchaseOrderDetail
from app.db.base import get_db
from app.models.PO_model import PurchaseOrder
from app.schemas.PO_detail_schema import PurchaseOrderDetailSchema, CreatePurchaseOrderDetailSchema, UpdatePurchaseOrderDetailSchema
from app.schemas.base_schema import DataResponse
from utils import get_product_variant_options

router = APIRouter()

@router.get("/purchase-order-details", tags=["purchase-order-details"], description="Get all purchase order details", response_model=DataResponse[list[PurchaseOrderDetailSchema]])
async def get_purchase_order_details(db: Session = Depends(get_db)):
    purchase_order_details = db.query(PurchaseOrderDetail).all()
    return DataResponse.custom_response(
        code="200", message="Get list purchase order details", data=purchase_order_details
    )

@router.get("/purchase-order-details/{purchase_order_detail_id}", tags=["purchase-order-details"], description="Get a purchase order detail by id", response_model=DataResponse[PurchaseOrderDetailSchema])
async def get_purchase_order_detail(purchase_order_detail_id: int, db: Session = Depends(get_db)):
    purchase_order_detail = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.id == purchase_order_detail_id).first()
    if not purchase_order_detail:
        return DataResponse.custom_response(
            code="404", message="Purchase order detail not found", data=None
        )
    return DataResponse.custom_response(
        code="200", message="Get purchase order detail by id", data=purchase_order_detail
    )

@router.post("/purchase-order-details", tags=["purchase-order-details"], description="Create a new purchase order detail", response_model=DataResponse[PurchaseOrderDetailSchema])
async def create_purchase_order_detail(data: CreatePurchaseOrderDetailSchema, db: Session = Depends(get_db)):
    purchase_order_detail = PurchaseOrderDetail(**data.dict())
    db.add(purchase_order_detail)
    db.commit()
    db.refresh(purchase_order_detail)
    return DataResponse.custom_response(
        code="201", message="Purchase order detail created successfully", data=purchase_order_detail
    )

@router.put("/purchase-order-details/{purchase_order_detail_id}", tags=["purchase-order-details"], description="Update a purchase order detail by id", response_model=DataResponse[PurchaseOrderDetailSchema])
async def update_purchase_order_detail(purchase_order_detail_id: int, data: UpdatePurchaseOrderDetailSchema, db: Session = Depends(get_db)):
    purchase_order_detail = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.id == purchase_order_detail_id).first()
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

@router.delete("/purchase-order-details/{purchase_order_detail_id}", tags=["purchase-order-details"], description="Delete a purchase order detail by id", response_model=DataResponse[None])
async def delete_purchase_order_detail(purchase_order_detail_id: int, db: Session = Depends(get_db)):
    purchase_order_detail = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.id == purchase_order_detail_id).first()
    if not purchase_order_detail:
        return DataResponse.custom_response(
            code="404", message="Purchase order detail not found", data=None
        )
    db.delete(purchase_order_detail)
    db.commit()
    return DataResponse.custom_response(
        code="200", message="Purchase order detail deleted by id", data=None
    )

# Get purchase_order options to dropdown input for purchase_order_detail creation
@router.get("/purchase-orders/options", tags=["purchase-order-details"], description="Get purchase_orders options for purchase_order_detail creation")
def order_options(db:Session = Depends(get_db)):
    return db.query(PurchaseOrder.purchase_order_id).all()

# Get variant options to dropdown input for purchase_order_detail creation
@router.get("/product-variants/options", tags=["purchase-order-details"], description="Get product_variant options for purchase_order_detail creation")
def variant_options(db:Session = Depends(get_db)):
    return get_product_variant_options(db)
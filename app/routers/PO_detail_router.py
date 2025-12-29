from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.PO_detail_model import PurchaseOrderDetail
from app.models.PO_model import PurchaseOrder
from app.db.base import get_db
from app.models.product_variant import ProductVariant
from app.schemas.PO_detail_schema import PurchaseOrderDetailSchema, CreatePurchaseOrderDetailSchema, UpdatePurchaseOrderDetailSchema
from app.schemas.base_schema import DataResponse
from app.services.product_variant_service import update_product_variant_stock_, update_product_variant_price_in_
from decimal import Decimal
router = APIRouter()

@router.get("/purchase-order-details", tags=["purchase-order-details"], description="Get all purchase order details", response_model=DataResponse[list[PurchaseOrderDetailSchema]])
async def get_purchase_order_details(db: Session = Depends(get_db)):
    purchase_order_details = db.query(PurchaseOrderDetail).all()
    return DataResponse.custom_response(
        code="200", message="Get list purchase order details", data=purchase_order_details
    )

@router.get("/purchase-order-details/{po_detail_id}", tags=["purchase-order-details"], description="Get a purchase order detail by id", response_model=DataResponse[PurchaseOrderDetailSchema])
async def get_purchase_order_detail(po_detail_id: int, db: Session = Depends(get_db)):
    purchase_order_detail = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.po_detail_id == po_detail_id).first()
    if not purchase_order_detail:
        return DataResponse.custom_response(
            code="404", message="Purchase order detail not found", data=None
        )
    return DataResponse.custom_response(
        code="200", message="Get purchase order detail by id", data=purchase_order_detail
    )

@router.post("/purchase-order-details", tags=["purchase-order-details"], description="Create a new purchase order detail", response_model=DataResponse[PurchaseOrderDetailSchema])
async def create_purchase_order_detail(data: CreatePurchaseOrderDetailSchema, db: Session = Depends(get_db)):
    variant = db.query(ProductVariant).filter(ProductVariant.variant_id == data.variant_id).first()
    purchase_order = db.query(PurchaseOrder).filter(PurchaseOrder.purchase_order_id == data.purchase_order_id).first()
    if not variant or not purchase_order:
        return DataResponse.custom_response(code="404", message="Product variant or purchase order not found", data=None)
    # Increase stock by the quantity in the PO detail (since this is a purchase order, stock increases)
    variant.stock_quantity += data.quantity
    update_product_variant_stock_(variant.variant_id, variant.stock_quantity, db)
    # Calculate price_in with the given formula
    price_in = (data.quantity * purchase_order.total_amount) / data.unit_price if data.unit_price else 0
    update_product_variant_price_in_(variant.variant_id, price_in, db)
    purchase_order_detail = PurchaseOrderDetail(**data.dict())
    db.add(purchase_order_detail)
    db.commit()
    db.refresh(purchase_order_detail)
    return DataResponse.custom_response(
        code="201", message="Purchase order detail created successfully", data=purchase_order_detail
    )

@router.put("/purchase-order-details/{po_detail_id}", tags=["purchase-order-details"], description="Update a purchase order detail by id", response_model=DataResponse[PurchaseOrderDetailSchema])
async def update_purchase_order_detail(po_detail_id: int, data: UpdatePurchaseOrderDetailSchema, db: Session = Depends(get_db)):
    purchase_order_detail = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.po_detail_id == po_detail_id).first()
    if not purchase_order_detail:
        return DataResponse.custom_response(
            code="404", message="Purchase order detail not found", data=None
        )
    variant = db.query(ProductVariant).filter(ProductVariant.variant_id == purchase_order_detail.variant_id).first()
    purchase_order = db.query(PurchaseOrder).filter(PurchaseOrder.purchase_order_id == purchase_order_detail.purchase_order_id).first()
    if not variant or not purchase_order:
        return DataResponse.custom_response(code="404", message="Product variant or purchase order not found", data=None)
    # Adjust stock: remove old quantity, add new quantity
    old_quantity = purchase_order_detail.quantity
    update_data = data.dict(exclude_unset=True)
    new_quantity = update_data.get("quantity", old_quantity)
    variant.stock_quantity = variant.stock_quantity - old_quantity + new_quantity
    update_product_variant_stock_(variant.variant_id, variant.stock_quantity, db)
    # Update price_in with the formula if unit_price or quantity is updated
    unit_price = update_data.get("unit_price", getattr(purchase_order_detail, "unit_price", 0))
    price_in = (new_quantity * purchase_order.total_amount) / unit_price if unit_price else 0
    update_product_variant_price_in_(variant.variant_id, price_in, db)
    for key, value in update_data.items():
        setattr(purchase_order_detail, key, value)
    db.commit()
    db.refresh(purchase_order_detail)
    return DataResponse.custom_response(
        code="200", message="Purchase order detail updated by id", data=purchase_order_detail
    )

@router.delete("/purchase-order-details/{po_detail_id}", tags=["purchase-order-details"], description="Delete a purchase order detail by id", response_model=DataResponse[None])
async def delete_purchase_order_detail(po_detail_id: int, db: Session = Depends(get_db)):
    purchase_order_detail = db.query(PurchaseOrderDetail).filter(PurchaseOrderDetail.po_detail_id == po_detail_id).first()
    if not purchase_order_detail:
        return DataResponse.custom_response(
            code="404", message="Purchase order detail not found", data=None
        )
    variant = db.query(ProductVariant).filter(ProductVariant.variant_id == purchase_order_detail.variant_id).first()
    if variant:
        # Decrease stock by the quantity in the PO detail (since deleting a purchase order, stock decreases)
        variant.stock_quantity -= purchase_order_detail.quantity
        update_product_variant_stock_(variant.variant_id, variant.stock_quantity, db)
        # Decrease price_in by the formula
        purchase_order = db.query(PurchaseOrder).filter(PurchaseOrder.purchase_order_id == purchase_order_detail.purchase_order_id).first()
        if purchase_order and purchase_order_detail.unit_price:
            from decimal import Decimal
            price_in_decrement = Decimal(purchase_order.total_amount) * Decimal(purchase_order_detail.quantity) / Decimal(purchase_order_detail.unit_price)
            new_price_in = Decimal(str(variant.price_in)) - price_in_decrement
            update_product_variant_price_in_(variant.variant_id, new_price_in, db)
    db.delete(purchase_order_detail)
    db.commit()
    return DataResponse.custom_response(
        code="200", message="Purchase order detail deleted by id", data=None
    )

#only update the quantity
@router.patch("/purchase-order-details/{po_detail_id}", tags=["purchase-order-details"], description="Update quantity of a purchase order detail", response_model=DataResponse[PurchaseOrderDetailSchema])
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
    

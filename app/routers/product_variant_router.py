from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.product_variant import ProductVariant
from app.schemas.product_variant_schema import ProductVariantSchema, CreateProductVariantSchema, UpdateProductVariantSchema
from app.schemas.base_schema import DataResponse
from app.services.product_variant_service import update_product_variant_stock_

router = APIRouter()

@router.get("/product-variants", tags=["product-variants"], description="Get all product variants", response_model=DataResponse[list[ProductVariantSchema]])
async def get_product_variants(db: Session = Depends(get_db)):
    product_variants = db.query(ProductVariant).all()
    return DataResponse.custom_response(
        code="200", message="Get list product variants", data=product_variants
    
    )
    
@router.get("/product-variants/{variant_id}", tags=["product-variants"], description="Get a product variant by id", response_model=DataResponse[ProductVariantSchema])
async def get_product_variant(variant_id: int, db: Session = Depends(get_db)):
    product_variant = db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()
    if not product_variant:
        return DataResponse.custom_response(
            code="404", message="Product variant not found", data=None
        )
    return DataResponse.custom_response(
        code="200", message="Get product variant", data=product_variant
    )

@router.post("/product-variants", tags=["product-variants"], description="Create a new product variant", response_model=DataResponse[ProductVariantSchema])
async def create_product_variant(data: CreateProductVariantSchema, db: Session = Depends(get_db)):
    product_variant = ProductVariant(**data.dict())
    db.add(product_variant)
    db.commit()
    db.refresh(product_variant)
    return DataResponse.custom_response(
        code="201", message="Product variant created successfully", data=product_variant
    )

@router.put("/product-variants/{variant_id}", tags=["product-variants"], description="Update a product variant by id", response_model=DataResponse[ProductVariantSchema])
async def update_product_variant(variant_id: int, data: UpdateProductVariantSchema, db: Session = Depends(get_db)):
    product_variant = db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()
    if not product_variant:
        return DataResponse.custom_response(
            code="404", message="Product variant not found", data=None
        )
    for key, value in data.dict().items():
        setattr(product_variant, key, value)
    db.commit()
    db.refresh(product_variant)
    return DataResponse.custom_response(
        code="200", message="Product variant updated successfully", data=product_variant
    )

@router.delete("/product-variants/{variant_id}", tags=["product-variants"], description="Delete a product variant by id", response_model=DataResponse[None])
async def delete_product_variant(variant_id: int, db: Session = Depends(get_db)):
    product_variant = db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()
    if not product_variant:
        return DataResponse.custom_response(
            code="404", message="Product variant not found", data=None
        )
    db.delete(product_variant)
    db.commit()
    return DataResponse.custom_response(
        code="200", message="Product variant deleted successfully", data=None
    )

#only update the stock_quantity
@router.patch("/product-variants/{variant_id}", tags=["product-variants"], description="Update stock quantity of a product variant", response_model=DataResponse[ProductVariantSchema])
async def update_product_variant_stock(variant_id: int, stock_quantity: int, db: Session = Depends(get_db)):
    update_product_variant_stock_(variant_id, stock_quantity, db)
    return DataResponse.custom_response(
        code="200", message="Product variant stock quantity updated successfully", data=db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()
    )
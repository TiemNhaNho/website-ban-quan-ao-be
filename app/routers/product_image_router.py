from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.product_model import Product
from app.models.product_image import ProductImage
from app.schemas.product_image_schema import ProductImageSchema, CreateProductImageSchema 
from app.schemas.base_schema import DataResponse
from utils import get_product_options

router = APIRouter()

@router.get("/product-images", tags=["product-images"], description="Get all product images", response_model=DataResponse[list[ProductImageSchema]])
async def get_product_images(db: Session = Depends(get_db)):
    product_images = db.query(ProductImage).all()
    return DataResponse.custom_response(
        code="200", message="Get list product images", data=product_images
    )

@router.get("/product-images/{product_image_id}", tags=["product-images"], description="Get a product image by id", response_model=DataResponse[ProductImageSchema])
async def get_product_image(product_image_id: int, db: Session = Depends(get_db)):
    product_image = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()
    if not product_image:
        return DataResponse.custom_response(
            code="404", message="Product image not found", data=None
        )
    return DataResponse.custom_response(
        code="200", message="Get product image by id", data=product_image
    )

@router.post("/product-images", tags=["product-images"], description="Create a new product image", response_model=DataResponse[ProductImageSchema])
async def create_product_image(data: CreateProductImageSchema, db: Session = Depends(get_db)):
    db_product_image = ProductImage(**data.dict())
    db.add(db_product_image)
    db.commit()
    db.refresh(db_product_image)
    return DataResponse.custom_response(
        code="201", message="Create product image", data=db_product_image
    )
    
@router.put("/product-images/{product_image_id}", tags=["product-images"], description="Update a product image by id", response_model=DataResponse[ProductImageSchema])
async def update_product_image(product_image_id: int, data: CreateProductImageSchema, db: Session = Depends(get_db)):
    product_image = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()
    if not product_image:
        return DataResponse.custom_response(
            code="404", message="Product image not found", data=None
        )

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product_image, key, value)

    db.commit()
    db.refresh(product_image)
    return DataResponse.custom_response(
        code="200", message="Update product image by id", data=product_image
    )

@router.delete("/product-images/{product_image_id}", tags=["product-images"], description="Delete a product image by id", response_model=DataResponse[None])
async def delete_product_image(product_image_id: int, db: Session = Depends(get_db)):
    product_image = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()
    if not product_image:
        return DataResponse.custom_response(
            code="404", message="Product image not found", data=None
        )
    db.delete(product_image)
    db.commit()
    return DataResponse.custom_response(
        code="200", message="Delete product image by id", data=None
    )
    
# Get product options to dropdown input for product_image creation
@router.get("/products/options", tags=["product-images"], description="Get product options for product_image creation")
def product_options(db:Session = Depends(get_db)):
    return get_product_options(db)
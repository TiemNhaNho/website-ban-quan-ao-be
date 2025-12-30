from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.product_review_model import ProductReview
from app.schemas.product_review_schema import ProductReviewSchema, CreateProductReviewSchema
from app.schemas.base_schema import DataResponse

router = APIRouter()

@router.get("/product-reviews", tags=["product-reviews"], description="Get all product reviews", response_model=DataResponse[list[ProductReviewSchema]])
async def get_product_reviews(db: Session = Depends(get_db)):
    product_reviews = db.query(ProductReview).all()
    return DataResponse.custom_response(
        code="200", message="Get list product reviews", data=product_reviews
    )

@router.get("/product-reviews/{review_id}", tags=["product-reviews"], description="Get a product review by id", response_model=DataResponse[ProductReviewSchema])
async def get_product_review(review_id: int, db: Session = Depends(get_db)):
    product_review = db.query(ProductReview).filter(ProductReview.review_id == review_id).first()
    if not product_review:
        return DataResponse.custom_response(
            code="404", message="Product review not found", data=None
        )
    return DataResponse.custom_response(
        code="200", message="Get product review by id", data=product_review
    )

@router.post("/product-reviews", tags=["product-reviews"], description="Create a new product review", response_model=DataResponse[ProductReviewSchema])
async def create_product_review(data: CreateProductReviewSchema, db: Session = Depends(get_db)):
    db_product_review = ProductReview(**data.dict())
    db.add(db_product_review)
    db.commit()
    db.refresh(db_product_review)
    return DataResponse.custom_response(
        code="201", message="Create product review", data=db_product_review
    )

@router.put("/product-reviews/{review_id}", tags=["product-reviews"], description="Update a product review by id", response_model=DataResponse[ProductReviewSchema])
async def update_product_review(review_id: int, data: CreateProductReviewSchema, db: Session = Depends(get_db)):
    product_review = db.query(ProductReview).filter(ProductReview.review_id == review_id).first()
    if not product_review:
        return DataResponse.custom_response(
            code="404", message="Product review not found", data=None
        )
    for key, value in data.dict().items():
        setattr(product_review, key, value)
    db.commit()
    db.refresh(product_review)
    return DataResponse.custom_response(
        code="200", message="Update product review", data=product_review
    )

@router.delete("/product-reviews/{review_id}", tags=["product-reviews"], description="Delete a product review by id", response_model=DataResponse[None])
async def delete_product_review(review_id: int, db: Session = Depends(get_db)):
    product_review = db.query(ProductReview).filter(ProductReview.review_id == review_id).first()
    if not product_review:
        return DataResponse.custom_response(
            code="404", message="Product review not found", data=None
        )
    db.delete(product_review)
    db.commit()
    return DataResponse.custom_response(
        code="200", message="Delete product review", data=None
    )

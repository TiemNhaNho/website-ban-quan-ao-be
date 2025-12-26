from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.category_model import Category
from app.schemas.category_schema import CategorySchema, CreateCategorySchema, UpdateCategorySchema
from app.schemas.base_schema import DataResponse

router = APIRouter()

@router.get(
    "/categories",
    tags=["categories"],
    description="Get all categories",
    response_model=DataResponse[list[CategorySchema]],
)
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return DataResponse.custom_response(
        code="200", message="Get list categories", data=categories
    )

@router.post(
    "/categories",
    tags=["categories"],
    description="Create a new category",
    response_model=DataResponse[CategorySchema],
)
async def create_category(data: CreateCategorySchema, db: Session = Depends(get_db)):
    db_category = Category(**data.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return DataResponse.custom_response(
        code="201", message="Create category", data=db_category
    )

@router.get(
    "/categories/{category_id}",
    tags=["categories"],
    description="Get a category by id",
    response_model=DataResponse[CategorySchema],
)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = (
        db.query(Category)
        .filter(Category.category_id == category_id)
        .first()
    )
    if not category:
        return DataResponse.custom_response(
            code="404", message="Category not found", data=None
        )
    return DataResponse.custom_response(
        code="200", message="Get category by id", data=category
    )

@router.delete(
    "/categories/{category_id}",
    tags=["categories"],
    description="Delete a category by id",
    response_model=DataResponse[CategorySchema],
)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = (
        db.query(Category)
        .filter(Category.category_id == category_id)
        .first()
    )
    if not category:
        return DataResponse.custom_response(
            code="404", message="Category not found", data=None
        )
    db.delete(category)
    db.commit()
    return DataResponse.custom_response(
        code="200", message="Delete category by id", data=None
    )

@router.put(
    "/categories/{category_id}",
    tags=["categories"],
    description="Update a category by id",
    response_model=DataResponse[CategorySchema],
)
def update_category(
    category_id: int, data: UpdateCategorySchema, db: Session = Depends(get_db)
):
    category = (
        db.query(Category)
        .filter(Category.category_id == category_id)
        .first()
    )
    if not category:
        return DataResponse.custom_response(
            code="404", message="Category not found", data=None
        )

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return DataResponse.custom_response(
        code="200", message="Update category by id", data=category
    )

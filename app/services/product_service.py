from sqlalchemy.orm import Session

from app.models.product_model import Product

# Get product options to dropdown input for product_image creation
def get_product_options(db: Session):
    return db.query(Product.product_id, Product.product_name).all()
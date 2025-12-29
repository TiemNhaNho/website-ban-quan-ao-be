from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.product_variant import ProductVariant

def update_product_variant_stock_(
    variant_id: int,
    stock_quantity: int,
    db: Session
):
    product_variant = db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()

    product_variant.stock_quantity = stock_quantity
    db.commit()
    db.refresh(product_variant)
    
def update_product_variant_price_in_(
    variant_id: int,
    price: Decimal,
    db: Session
):
    product_variant = db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()

    product_variant.price_in = price
    db.commit()
    db.refresh(product_variant)
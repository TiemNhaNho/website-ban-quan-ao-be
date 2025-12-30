from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.category_model import Category
from app.models.customer_model import Customer
from app.models.product_model import Product
from app.models.product_variant_model import ProductVariant
from app.models.supplier_model import Supplier
from app.models.PO_model import PurchaseOrder
from app.models.coupon_model import Coupon
from app.models.shipping_method_model import ShippingMethod
from app.models.order_model import Order

router = APIRouter()

@router.get("/products-select/options", tags=["FK-dropdown-options"], description="get products options")
def product_options(db: Session = Depends(get_db)):
    product = db.query(Product.product_id.label("value"), Product.product_name.label("label")).all()
    return [{"product_id": p.value, "product_name": p.label} for p in product]

@router.get("/categories-select/options", tags=["FK-dropdown-options"], description="get categories options")
def category_options(db: Session = Depends(get_db)):
    category = db.query(Category.category_id.label("value"), Category.category_name.label("label")).all()
    return [{"category_id": c.value, "category_name": c.label} for c in category]

@router.get("/suppliers-select/options", tags=["FK-dropdown-options"], description="get suppliers options")
def supplier_options(db: Session = Depends(get_db)):
    supplier = db.query(Supplier.supplier_id.label("value"), Supplier.supplier_name.label("label")).all()
    return [{"supplier_id": s.value, "supplier_name": s.label} for s in supplier]

@router.get("/purchase-orders-select/options", tags=["FK-dropdown-options"], description="get purchase-orders options")
def purchase_order_options(db: Session = Depends(get_db)):
    purchase_order = db.query(PurchaseOrder.purchase_order_id.label('value')).all()
    return [{"purchase_order_id": po.value} for po in purchase_order]

@router.get("/product-variants-select/options", tags=["FK-dropdown-options"], description="get product-variants options")
def product_variant_options(db: Session = Depends(get_db)):
    product_variants = db.query(ProductVariant.variant_id.label("value"), Product.product_name.label("label")).join(Product, Product.product_id == ProductVariant.product_id).all()
    return [{"variant_id": pv.value, "product_name": pv.label} for pv in product_variants]

@router.get("/customers-select/options", tags=["FK-dropdown-options"], description="get customers options")
def customer_options(db: Session = Depends(get_db)):
    customers = db.query(Customer.id.label("value"), Customer.username.label("label")).all()
    return [{"id": c.value, "username": c.label} for c in customers]

@router.get("/coupons-select/options", tags=["FK-dropdown-options"], description="get coupons options")
def coupon_options(db: Session = Depends(get_db)):
    coupon = db.query(Coupon.coupon_id.label('value'), Coupon.code.label('label')).all()
    return [{"coupon_id": c.value, "code": c.label} for c in coupon]

@router.get("/shipping-methods-select/options", tags=["FK-dropdown-options"], description="get shipping-methods options")
def shipping_method_options(db: Session = Depends(get_db)):
    shipping = db.query(ShippingMethod.shipping_method_id.label('value'), ShippingMethod.method_name.label('label')).all()
    return [{"shipping_method_id": s.value, "method_name": s.label} for s in shipping]

@router.get("/orders-select/options", tags=["FK-dropdown-options"], description="get orders options")
def order_options(db: Session = Depends(get_db)):
    order = db.query(Order.order_id.label('value')).all()
    return [{"order_id": o.value} for o in order]
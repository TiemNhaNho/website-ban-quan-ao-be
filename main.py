import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.base import engine
from app.models import Base
from app.routers.customer_router import router as customer_router
from app.routers.product_router import router as product_router
from app.routers.category_router import router as category_router
from app.routers.cart_router import router as cart_router
from app.routers.order_router import router as order_router
from app.routers.product_image_router import router as product_image_router
from app.routers.product_variant_router import router as product_variant_router 
from app.routers.product_review_router import router as product_review_router
from app.routers.order_detail_router import router as order_detail_router
from app.routers.PO_detail_router import router as purchase_order_detail_router
from app.routers.PO_router import router as purchase_order_router
from app.routers.supplier_router import router as supplier_router
from app.routers.coupon_router import router as coupon_router
from app.routers.shipping_method_router import router as shipping_method_router
from app.routers.dropdown_foreign_key_router import router as dropdown_fk_router

Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(
    title="Tiem Nha Nho API",
    description="API for Tiem Nha Nho - Fashion's Clothing Store",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(cart_router)
app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(shipping_method_router)
app.include_router(coupon_router)

app.include_router(customer_router)

app.include_router(order_detail_router)
app.include_router(order_router)
app.include_router(product_image_router)
app.include_router(product_review_router)
app.include_router(product_router)
app.include_router(product_variant_router)
app.include_router(purchase_order_detail_router)
app.include_router(purchase_order_router)

app.include_router(dropdown_fk_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Tiem Nha Nho API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=settings.reload)
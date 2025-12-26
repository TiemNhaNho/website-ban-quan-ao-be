from fastapi import FastAPI
from app.db.base import engine
from app.models import Base
from app.routers.customer_router import router as customer_router
from app.routers.product_router import router as product_router
from app.routers.category_router import router as category_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tiem Nha Nho API",
    description="API for Tiem Nha Nho - Fashion's Clothing Store",
)

app.include_router(customer_router)
app.include_router(product_router)
app.include_router(category_router)

@app.get("/home")
async def root():
    return {"message": "Hello World class A"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
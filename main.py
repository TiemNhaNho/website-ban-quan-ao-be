from fastapi import FastAPI
from app.db.base import engine
from app.models import Base
from app.routers.customer_router import router as customer_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tiem Nha Nho API",
    description="API for Tiem Nha Nho - Fashion's Clothing Store",
)

app.include_router(customer_router)

@app.get("/home")
async def root():
    return {"message": "Hello World class A"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
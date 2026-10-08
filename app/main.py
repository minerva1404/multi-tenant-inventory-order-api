from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes import auth, inventory, orders, products
from app.db.session import engine

app = FastAPI(
    title="Multi-Tenant Inventory & Order API",
    version="1.0.0",
    description=(
        "A production-oriented multi-tenant inventory and order API "
        "with JWT authentication, role-based access control, "
        "inventory transactions, and tenant isolation."
    ),
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(orders.router)


@app.get("/", tags=["System"])
def read_root():
    return {
        "message": "Multi-Tenant Inventory & Order API is running",
        "version": "1.0.0",
    }


@app.get("/health", tags=["System"])
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
    }

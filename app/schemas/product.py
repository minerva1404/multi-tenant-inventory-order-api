from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=160)
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
class ProductResponse(ProductCreate):
    id: int
    model_config = {"from_attributes": True}
class InventoryAdjustRequest(BaseModel):
    quantity: int = Field(ne=0)
    reason: str = Field(min_length=1, max_length=100)
class InventoryResponse(BaseModel):
    product_id: int
    quantity: int
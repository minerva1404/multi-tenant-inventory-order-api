from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_current_user, require_admin
from app.db.session import get_db
from app.models.inventory import InventoryItem
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])
@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
):
    existing = (
        db.query(Product)
        .filter(
            Product.tenant_id == current_user.tenant_id,
            Product.sku == payload.sku,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="SKU already exists",
        )
    try:
        product = Product(
            tenant_id=current_user.tenant_id,
            sku=payload.sku,
            name=payload.name,
            price=payload.price,
        )
        db.add(product)
        db.flush()
        db.add(
            InventoryItem(
                tenant_id=current_user.tenant_id,
                product_id=product.id,
                quantity=0,
            )
        )
        db.commit()
        db.refresh(product)
        return product
    except Exception:
        db.rollback()
        raise
@router.get("", response_model=list[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return (
        db.query(Product)
        .filter(Product.tenant_id == current_user.tenant_id)
        .order_by(Product.id)
        .all()
    )
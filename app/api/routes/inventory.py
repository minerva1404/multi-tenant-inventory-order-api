from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_current_user, require_admin
from app.db.session import get_db
from app.models.inventory import InventoryItem, InventoryMovement
from app.models.product import Product
from app.schemas.product import InventoryAdjustRequest, InventoryResponse

router = APIRouter(prefix="/inventory", tags=["Inventory"])
@router.get("/{product_id}", response_model=InventoryResponse)
def get_inventory(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    item = (
        db.query(InventoryItem)
        .filter(
            InventoryItem.product_id == product_id,
            InventoryItem.tenant_id == current_user.tenant_id,
        )
        .first()
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found",
        )
    return InventoryResponse(
        product_id=item.product_id,
        quantity=item.quantity,
    )
@router.post(
    "/{product_id}/adjust",
    response_model=InventoryResponse,
)
def adjust_inventory(
    product_id: int,
    payload: InventoryAdjustRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
):
    product = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.tenant_id == current_user.tenant_id,
        )
        .first()
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    item = (
        db.query(InventoryItem)
        .filter(
            InventoryItem.product_id == product_id,
            InventoryItem.tenant_id == current_user.tenant_id,
        )
        .with_for_update()
        .first()
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found",
        )
    new_quantity = item.quantity + payload.quantity
    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Insufficient inventory",
        )
    try:
        item.quantity = new_quantity
        db.add(
            InventoryMovement(
                tenant_id=current_user.tenant_id,
                product_id=product_id,
                change=payload.quantity,
                reason=payload.reason,
            )
        )
        db.commit()
        db.refresh(item)
        return InventoryResponse(
            product_id=item.product_id,
            quantity=item.quantity,
        )
    except Exception:
        db.rollback()
        raise
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_current_user
from app.db.session import get_db
from app.models.inventory import InventoryItem, InventoryMovement
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])
@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    product_ids = [item.product_id for item in payload.items]
    if len(product_ids) != len(set(product_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Each product can appear only once per order",
        )
    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == current_user.tenant_id,
            Product.id.in_(product_ids),
        )
        .all()
    )
    products_by_id = {product.id: product for product in products}
    if len(products_by_id) != len(product_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more products not found",
        )
    # Lock inventory rows in deterministic product-id order.
    # This reduces the chance of deadlocks when concurrent orders
    # affect multiple products.
    locked_inventory = (
        db.query(InventoryItem)
        .filter(
            InventoryItem.tenant_id == current_user.tenant_id,
            InventoryItem.product_id.in_(product_ids),
        )
        .order_by(InventoryItem.product_id)
        .with_for_update()
        .all()
    )
    inventory_by_product = {
        item.product_id: item for item in locked_inventory
    }
    if len(inventory_by_product) != len(product_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory missing for a product",
        )
    # Validate the entire order before creating any database records.
    for requested in payload.items:
        product = products_by_id[requested.product_id]
        inventory = inventory_by_product[requested.product_id]
        if inventory.quantity < requested.quantity:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Insufficient inventory for SKU {product.sku}",
            )
    try:
        total = Decimal(0)
        order = Order(
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            status="confirmed",
            total_amount=Decimal(0),
        )
        db.add(order)
        db.flush()
        response_items = []
        for requested in payload.items:
            product = products_by_id[requested.product_id]
            inventory = inventory_by_product[requested.product_id]
            line_total = product.price * requested.quantity
            inventory.quantity -= requested.quantity
            total += line_total
            db.add(
                InventoryMovement(
                    tenant_id=current_user.tenant_id,
                    product_id=product.id,
                    change=-requested.quantity,
                    reason=f"order:{order.id}",
                )
            )
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=requested.quantity,
                    unit_price=product.price,
                    line_total=line_total,
                )
            )
            response_items.append(
                {
                    "product_id": product.id,
                    "quantity": requested.quantity,
                    "unit_price": product.price,
                    "line_total": line_total,
                }
            )
        order.total_amount = total
        db.commit()
        db.refresh(order)
        return OrderResponse(
            id=order.id,
            status=order.status,
            total_amount=order.total_amount,
            items=response_items,
        )
    except Exception:
        db.rollback()
        raise
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.tenant_id == current_user.tenant_id,
        )
        .first()
    )
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return OrderResponse(
        id=order.id,
        status=order.status,
        total_amount=order.total_amount,
        items=[
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "line_total": item.line_total,
            }
            for item in order.items
        ],
    )
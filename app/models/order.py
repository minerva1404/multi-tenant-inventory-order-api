from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Order(Base):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "total_amount >= 0",
            name="ck_order_total_nonnegative",
        ),
        Index(
            "ix_order_tenant_created_at",
            "tenant_id",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="confirmed",
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    tenant = relationship(
        "Tenant",
        back_populates="orders",
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_order_item_quantity_positive",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="ck_order_item_unit_price_nonnegative",
        ),
        CheckConstraint(
            "line_total >= 0",
            name="ck_order_item_line_total_nonnegative",
        ),
        Index(
            "ix_order_item_order_product",
            "order_id",
            "product_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        index=True,
    )

    quantity: Mapped[int] = mapped_column(Integer)

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
    )

    order = relationship(
        "Order",
        back_populates="items",
    )

    product = relationship(
        "Product",
        back_populates="order_items",
    )
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "product_id",
            name="uq_inventory_tenant_product",
        ),
        CheckConstraint(
            "quantity >= 0",
            name="ck_inventory_quantity_nonnegative",
        ),
        Index(
            "ix_inventory_tenant_product",
            "tenant_id",
            "product_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    tenant = relationship(
        "Tenant",
        back_populates="inventory_items",
    )

    product = relationship(
        "Product",
        back_populates="inventory",
    )


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    __table_args__ = (
        Index(
            "ix_inventory_movement_tenant_product",
            "tenant_id",
            "product_id",
        ),
        Index(
            "ix_inventory_movement_created_at",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        index=True,
    )

    change: Mapped[int] = mapped_column(Integer)

    reason: Mapped[str] = mapped_column(
        String(100),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
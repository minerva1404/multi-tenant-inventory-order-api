from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "sku",
            name="uq_product_tenant_sku",
        ),
        Index(
            "ix_product_tenant_name",
            "tenant_id",
            "name",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        index=True,
    )

    sku: Mapped[str] = mapped_column(
        String(80),
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(160),
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    tenant = relationship(
        "Tenant",
        back_populates="products",
    )

    inventory = relationship(
        "InventoryItem",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product",
    )
from datetime import datetime, timezone

from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Tenant(Base):
    __tablename__ = "tenants"

    __table_args__ = (
        Index(
            "ix_tenant_name",
            "name",
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(120),
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    users = relationship(
        "User",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    products = relationship(
        "Product",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    inventory_items = relationship(
        "InventoryItem",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    orders = relationship(
        "Order",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
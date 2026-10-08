from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint(
            "email",
            name="uq_user_email",
        ),
        Index(
            "ix_user_tenant_email",
            "tenant_id",
            "email",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(512),
    )

    role: Mapped[str] = mapped_column(
        String(30),
        default="member",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    tenant = relationship(
        "Tenant",
        back_populates="users",
    )
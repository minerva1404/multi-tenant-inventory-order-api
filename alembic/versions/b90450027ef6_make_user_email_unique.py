"""make user email unique

Revision ID: b90450027ef6
Revises: 0001_initial
Create Date: 2026-10-06 22:13:38
"""

from collections.abc import Sequence

from alembic import op

revision: str = "b90450027ef6"
down_revision: str | Sequence[str] | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_user_email",
        "users",
        ["email"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_user_email",
        "users",
        type_="unique",
    )
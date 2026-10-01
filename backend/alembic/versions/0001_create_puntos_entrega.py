"""crear tabla puntos_entrega

Revision ID: 0001
Revises:
Create Date: 2026-09-24

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.create_table(
        "puntos_entrega",
        sa.Column(
            "punto_id",
            sa.Uuid(),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("direccion", sa.Text(), nullable=False),
        sa.Column("latitud", sa.Numeric(precision=9, scale=6), nullable=False),
        sa.Column("longitud", sa.Numeric(precision=9, scale=6), nullable=False),
        sa.Column("distrito", sa.String(length=100), nullable=False),
        sa.Column(
            "estado",
            sa.String(length=20),
            nullable=False,
            server_default="ACTIVO",
        ),
    )
    op.create_index("idx_puntos_entrega_distrito", "puntos_entrega", ["distrito"])


def downgrade() -> None:
    op.drop_index("idx_puntos_entrega_distrito", table_name="puntos_entrega")
    op.drop_table("puntos_entrega")

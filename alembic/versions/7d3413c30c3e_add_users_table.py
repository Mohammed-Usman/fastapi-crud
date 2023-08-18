"""add users table

Revision ID: 7d3413c30c3e
Revises: 0c8546342476
Create Date: 2023-08-18 16:39:23.664168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d3413c30c3e'
down_revision: Union[str, None] = '0c8546342476'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("created_at",
                  sa.TIMESTAMP(timezone=True),
                  server_default=sa.text("now()"),
                  nullable=False
                  ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass

"""add content column to posts table

Revision ID: 0c8546342476
Revises: 437f76cbefe0
Create Date: 2023-08-18 16:28:49.130799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c8546342476'
down_revision: Union[str, None] = '437f76cbefe0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

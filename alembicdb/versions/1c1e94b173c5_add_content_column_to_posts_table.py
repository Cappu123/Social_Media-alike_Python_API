"""add content column to posts table

Revision ID: 1c1e94b173c5
Revises: f4f13c008d87
Create Date: 2024-07-11 10:28:06.261576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c1e94b173c5'
down_revision: Union[str, None] = 'f4f13c008d87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

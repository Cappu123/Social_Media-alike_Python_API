"""create user table

Revision ID: e93211374450
Revises: 1c1e94b173c5
Create Date: 2024-07-11 10:49:02.468114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e93211374450'
down_revision: Union[str, None] = '1c1e94b173c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('now()'), nullable=False),
                              sa.PrimaryKeyConstraint('id'),
                              sa.UniqueConstraint('email')
                              )
    pass


def downgrade():
    op.drop_table('users')
    pass

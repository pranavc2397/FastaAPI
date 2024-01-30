"""create posts table

Revision ID: 33b998927402
Revises: 
Create Date: 2024-01-26 19:56:48.372634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33b998927402'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable = False, 
                                      primary_key=True),sa.Column('title',sa.String(),nullable = False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass

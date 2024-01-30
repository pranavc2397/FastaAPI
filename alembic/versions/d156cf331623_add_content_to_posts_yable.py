"""add content to posts yable

Revision ID: d156cf331623
Revises: 33b998927402
Create Date: 2024-01-26 20:28:41.017575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd156cf331623'
down_revision: Union[str, None] = '33b998927402'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass

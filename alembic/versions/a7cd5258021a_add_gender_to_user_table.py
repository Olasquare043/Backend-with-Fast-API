"""add gender to user table

Revision ID: a7cd5258021a
Revises: b0d518e458f8
Create Date: 2025-10-27 11:07:06.911501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7cd5258021a'
down_revision: Union[str, Sequence[str], None] = 'b0d518e458f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""ALTER TABLE users
               ADD COLUMN gender varchar(100) DEFAULT 'male' 
               """)
    pass


def downgrade() -> None:
    op.execute("""ALTER TABLE users
               DROP COLUMN gender """)
    pass

"""update user detail

Revision ID: 4e17dc70277d
Revises: a7cd5258021a
Create Date: 2025-10-29 12:00:18.545997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e17dc70277d'
down_revision: Union[str, Sequence[str], None] = 'a7cd5258021a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""ALTER TABLE users
               ADD COLUMN userType varchar(100) DEFAULT 'student' 
               """)


def downgrade() -> None:
    op.execute("""ALTER TABLE users
               DROP COLUMN userType
                """)
    pass

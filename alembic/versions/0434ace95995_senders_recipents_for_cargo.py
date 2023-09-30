"""senders-recipents for cargo

Revision ID: 0434ace95995
Revises: a11e4c1a7b0e
Create Date: 2023-09-29 15:26:50.798206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0434ace95995'
down_revision: Union[str, None] = 'a11e4c1a7b0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

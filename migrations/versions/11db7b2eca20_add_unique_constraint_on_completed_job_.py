"""Add unique constraint on completed_job_id and trigger_job_id

Revision ID: 11db7b2eca20
Revises: 9b8ed3c5e33a
Create Date: 2025-04-15 22:49:01.310044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11db7b2eca20'
down_revision: Union[str, None] = '9b8ed3c5e33a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

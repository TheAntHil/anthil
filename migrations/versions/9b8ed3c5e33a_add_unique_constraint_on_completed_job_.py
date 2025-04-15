"""Add unique constraint on completed_job_id and trigger_job_id

Revision ID: 9b8ed3c5e33a
Revises: 8ef3f82c89db
Create Date: 2025-04-15 22:46:20.596891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b8ed3c5e33a'
down_revision: Union[str, None] = '8ef3f82c89db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

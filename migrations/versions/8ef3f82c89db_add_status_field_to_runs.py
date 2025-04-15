# filepath: d:\Dev\pet\Anthillproject\anthil\migrations\versions\8ef3f82c89db_add_status_field_to_runs.py
"""Add status field to runs

Revision ID: 8ef3f82c89db
Revises: 4ab78808b281
Create Date: 2025-04-14 18:12:53.742225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ef3f82c89db'
down_revision: Union[str, None] = '4ab78808b281'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE run_status AS ENUM ('created', 'scheduled', 'triggered')")
    op.execute("""
        ALTER TABLE runs
        ALTER COLUMN status TYPE run_status
        USING status::run_status
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE runs
        ALTER COLUMN status TYPE VARCHAR(50)
    """)
    op.execute("DROP TYPE run_status")

"""Make schedule date optional

Revision ID: make_schedule_date_optional
Revises: add_icons_table
Create Date: 2025-12-03 10:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'make_schedule_date_optional'
down_revision = 'add_icons_table'
branch_labels = None
depends_on = None


def upgrade():
    # Make date column nullable
    # For SQLite, we need to recreate the table
    bind = op.get_bind()
    if bind.dialect.name == 'sqlite':
        # SQLite doesn't support ALTER COLUMN, so we need to recreate the table
        with op.batch_alter_table('schedules', schema=None) as batch_op:
            batch_op.alter_column('date', nullable=True)
    else:
        # For PostgreSQL and others, we can use alter_column
        op.alter_column('schedules', 'date', nullable=True)


def downgrade():
    # Make date column required again
    # For SQLite, we need to recreate the table
    bind = op.get_bind()
    if bind.dialect.name == 'sqlite':
        with op.batch_alter_table('schedules', schema=None) as batch_op:
            # Set default date for any NULL values before making it required
            op.execute(text("UPDATE schedules SET date = date('now') WHERE date IS NULL"))
            batch_op.alter_column('date', nullable=False)
    else:
        # For PostgreSQL and others
        op.execute(text("UPDATE schedules SET date = CURRENT_DATE WHERE date IS NULL"))
        op.alter_column('schedules', 'date', nullable=False)


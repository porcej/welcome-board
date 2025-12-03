"""Add show_name field to schedule

Revision ID: add_show_name_to_schedule
Revises: add_background_image_size
Create Date: 2025-12-02 23:20:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'add_show_name_to_schedule'
down_revision = 'add_background_image_size'
branch_labels = None
depends_on = None


def column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    bind = op.get_bind()
    # For SQLite, use PRAGMA table_info
    if bind.dialect.name == 'sqlite':
        result = bind.execute(text(f'PRAGMA table_info("{table_name}")'))
        columns = [row[1] for row in result]
        return column_name in columns
    else:
        # For PostgreSQL and others
        from sqlalchemy import inspect
        insp = inspect(bind)
        columns = [col['name'] for col in insp.get_columns(table_name)]
        return column_name in columns


def upgrade():
    # Add show_name field if it doesn't exist
    if not column_exists('schedules', 'show_name'):
        op.add_column('schedules', sa.Column('show_name', sa.Boolean(), nullable=True))
        op.execute(text("UPDATE schedules SET show_name = 1 WHERE show_name IS NULL"))


def downgrade():
    if column_exists('schedules', 'show_name'):
        op.drop_column('schedules', 'show_name')


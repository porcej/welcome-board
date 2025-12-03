"""Add schedule color field to settings

Revision ID: add_schedule_color
Revises: add_logo_size
Create Date: 2025-12-02 22:40:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'add_schedule_color'
down_revision = 'add_logo_size'
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
    # Add schedule_color field if it doesn't exist
    if not column_exists('site_settings', 'schedule_color'):
        op.add_column('site_settings', sa.Column('schedule_color', sa.String(length=7), nullable=True))
        # Set default value for existing rows (same as box_color or default)
        op.execute(text("UPDATE site_settings SET schedule_color = COALESCE(box_color, '#212529') WHERE schedule_color IS NULL"))


def downgrade():
    if column_exists('site_settings', 'schedule_color'):
        op.drop_column('site_settings', 'schedule_color')


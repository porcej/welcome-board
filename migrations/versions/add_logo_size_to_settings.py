"""Add logo size field to settings

Revision ID: add_logo_size
Revises: add_color_fields
Create Date: 2025-12-02 22:30:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'add_logo_size'
down_revision = 'add_color_fields'
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
    # Add logo_size field if it doesn't exist
    if not column_exists('site_settings', 'logo_size'):
        op.add_column('site_settings', sa.Column('logo_size', sa.Integer(), nullable=True))
        # Set default value for existing rows
        op.execute(text("UPDATE site_settings SET logo_size = 120 WHERE logo_size IS NULL"))


def downgrade():
    if column_exists('site_settings', 'logo_size'):
        op.drop_column('site_settings', 'logo_size')


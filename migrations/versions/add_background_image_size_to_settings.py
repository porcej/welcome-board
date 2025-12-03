"""Add background image size field to settings

Revision ID: add_background_image_size
Revises: add_opacity_fields
Create Date: 2025-12-02 23:10:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'add_background_image_size'
down_revision = 'add_opacity_fields'
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
    # Add background_image_size field if it doesn't exist
    if not column_exists('site_settings', 'background_image_size'):
        op.add_column('site_settings', sa.Column('background_image_size', sa.String(length=20), nullable=True))
        op.execute(text("UPDATE site_settings SET background_image_size = 'center' WHERE background_image_size IS NULL"))


def downgrade():
    if column_exists('site_settings', 'background_image_size'):
        op.drop_column('site_settings', 'background_image_size')


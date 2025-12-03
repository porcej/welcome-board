"""Add color customization fields to settings

Revision ID: add_color_fields
Revises: b03924e39223
Create Date: 2025-12-02 22:20:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'add_color_fields'
down_revision = 'b03924e39223'
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
    # Add color fields if they don't exist
    if not column_exists('site_settings', 'bg_color'):
        op.add_column('site_settings', sa.Column('bg_color', sa.String(length=7), nullable=True))
    if not column_exists('site_settings', 'text_color'):
        op.add_column('site_settings', sa.Column('text_color', sa.String(length=7), nullable=True))
    if not column_exists('site_settings', 'box_color'):
        op.add_column('site_settings', sa.Column('box_color', sa.String(length=7), nullable=True))


def downgrade():
    if column_exists('site_settings', 'box_color'):
        op.drop_column('site_settings', 'box_color')
    if column_exists('site_settings', 'text_color'):
        op.drop_column('site_settings', 'text_color')
    if column_exists('site_settings', 'bg_color'):
        op.drop_column('site_settings', 'bg_color')


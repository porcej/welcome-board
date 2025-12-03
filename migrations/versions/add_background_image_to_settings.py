"""Add background image field to settings

Revision ID: add_background_image
Revises: add_schedule_color
Create Date: 2025-12-02 22:50:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'add_background_image'
down_revision = 'add_schedule_color'
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
    # Add background_image_path field if it doesn't exist
    if not column_exists('site_settings', 'background_image_path'):
        op.add_column('site_settings', sa.Column('background_image_path', sa.String(length=512), nullable=True))


def downgrade():
    if column_exists('site_settings', 'background_image_path'):
        op.drop_column('site_settings', 'background_image_path')


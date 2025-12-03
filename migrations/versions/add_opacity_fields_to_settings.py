"""Add opacity fields to settings

Revision ID: add_opacity_fields
Revises: add_background_image
Create Date: 2025-12-02 23:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'add_opacity_fields'
down_revision = 'add_background_image'
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
    # Add opacity fields if they don't exist
    if not column_exists('site_settings', 'box_opacity'):
        op.add_column('site_settings', sa.Column('box_opacity', sa.Float(), nullable=True))
        op.execute(text("UPDATE site_settings SET box_opacity = 1.0 WHERE box_opacity IS NULL"))
    if not column_exists('site_settings', 'schedule_opacity'):
        op.add_column('site_settings', sa.Column('schedule_opacity', sa.Float(), nullable=True))
        op.execute(text("UPDATE site_settings SET schedule_opacity = 1.0 WHERE schedule_opacity IS NULL"))


def downgrade():
    if column_exists('site_settings', 'schedule_opacity'):
        op.drop_column('site_settings', 'schedule_opacity')
    if column_exists('site_settings', 'box_opacity'):
        op.drop_column('site_settings', 'box_opacity')


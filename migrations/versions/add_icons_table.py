"""Add icons table

Revision ID: add_icons_table
Revises: add_show_name_to_schedule
Create Date: 2025-12-02 23:30:00
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_icons_table'
down_revision = 'add_show_name_to_schedule'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'icons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('image_path', sa.String(length=512), nullable=True),
        sa.Column('characters', sa.String(length=50), nullable=True),
        sa.Column('font', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_icons_name', 'icons', ['name'], unique=True)


def downgrade():
    op.drop_index('ix_icons_name', table_name='icons')
    op.drop_table('icons')


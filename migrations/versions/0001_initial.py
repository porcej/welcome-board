"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2025-11-16 00:00:00
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("1")),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
    )
    op.create_index("ix_schedules_date", "schedules", ["date"], unique=False)

    op.create_table(
        "schedule_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("schedule_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("end_time", sa.Time(), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("uniform", sa.String(length=255), nullable=True),
        sa.Column("lead", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("icon", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["schedule_id"], ["schedules.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_schedule_items_schedule_id", "schedule_items", ["schedule_id"], unique=False)

    op.create_table(
        "site_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("logo_path", sa.String(length=512), nullable=True),
        sa.Column("notes_left_col", sa.Text(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("timezone", sa.String(length=64), nullable=True),
    )

    op.create_table(
        "weather_cache",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("date_key", sa.String(length=32), nullable=False),
        sa.Column("morning_json", sa.Text(), nullable=True),
        sa.Column("noon_json", sa.Text(), nullable=True),
        sa.Column("afternoon_json", sa.Text(), nullable=True),
        sa.Column("fetched_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_weather_cache_date_key", "weather_cache", ["date_key"], unique=False)


def downgrade():
    op.drop_index("ix_weather_cache_date_key", table_name="weather_cache")
    op.drop_table("weather_cache")
    op.drop_table("site_settings")
    op.drop_index("ix_schedule_items_schedule_id", table_name="schedule_items")
    op.drop_table("schedule_items")
    op.drop_index("ix_schedules_date", table_name="schedules")
    op.drop_table("schedules")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")



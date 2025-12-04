from datetime import datetime, timedelta
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db, login_manager


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True, nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id: str) -> Optional["User"]:
    return User.query.get(int(user_id))


class Schedule(TimestampMixin, db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=True, index=True)  # Optional: if provided, schedule is only active on that date
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    show_name = db.Column(db.Boolean, default=True, nullable=False)  # Whether to display name on sign
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    created_by_user = db.relationship("User", backref=db.backref("schedules", lazy=True))


class Icon(TimestampMixin, db.Model):
    __tablename__ = "icons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    image_path = db.Column(db.String(512), nullable=True)  # Path to uploaded image
    characters = db.Column(db.String(50), nullable=True)  # Text characters for text-based icon
    font = db.Column(db.String(100), nullable=True)  # Font family name

    def __repr__(self):
        return f"<Icon {self.name}>"


class ScheduleItem(TimestampMixin, db.Model):
    __tablename__ = "schedule_items"
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedules.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    uniform = db.Column(db.String(255), nullable=True)
    lead = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(255), nullable=True)  # Can be built-in icon name or Icon.name

    schedule = db.relationship("Schedule", backref=db.backref("items", lazy=True, cascade="all, delete-orphan"))

    def compute_end_time(self) -> None:
        if self.start_time and self.duration_minutes is not None:
            dt = datetime.combine(datetime.utcnow().date(), self.start_time)
            dt_end = dt + timedelta(minutes=self.duration_minutes)
            self.end_time = dt_end.time()


class SiteSettings(TimestampMixin, db.Model):
    __tablename__ = "site_settings"
    id = db.Column(db.Integer, primary_key=True)
    logo_path = db.Column(db.String(512), nullable=True)
    logo_size = db.Column(db.Integer, nullable=True, default=120)  # Max height in pixels
    background_image_path = db.Column(db.String(512), nullable=True)
    background_image_size = db.Column(db.String(20), nullable=True, default="center")  # tile, stretch, fit, center
    notes_left_col = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    timezone = db.Column(db.String(64), nullable=True)
    bg_color = db.Column(db.String(7), nullable=True, default="#000000")  # Hex color for background
    text_color = db.Column(db.String(7), nullable=True, default="#ffffff")  # Hex color for text
    box_color = db.Column(db.String(7), nullable=True, default="#212529")  # Hex color for side panel
    box_opacity = db.Column(db.Float, nullable=True, default=1.0)  # Opacity for side panel (0.0-1.0)
    schedule_color = db.Column(db.String(7), nullable=True, default="#212529")  # Hex color for schedule box
    schedule_opacity = db.Column(db.Float, nullable=True, default=1.0)  # Opacity for schedule box (0.0-1.0)


class WeatherCache(TimestampMixin, db.Model):
    __tablename__ = "weather_cache"
    id = db.Column(db.Integer, primary_key=True)
    date_key = db.Column(db.String(32), nullable=False, index=True)  # e.g., YYYY-MM-DD
    morning_json = db.Column(db.Text, nullable=True)
    noon_json = db.Column(db.Text, nullable=True)
    afternoon_json = db.Column(db.Text, nullable=True)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)



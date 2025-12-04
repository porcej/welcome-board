from flask import render_template, jsonify
from . import display_bp
from ..models import Schedule, ScheduleItem, SiteSettings, Icon
from ..services.weather import get_weather


@display_bp.route("/")
def sign():
    settings = SiteSettings.query.first()
    active = Schedule.query.filter_by(is_active=True).order_by(Schedule.date.desc()).first()
    items = []
    if active:
        items = ScheduleItem.query.filter_by(schedule_id=active.id).order_by(ScheduleItem.start_time).all()
    weather = get_weather(settings.latitude if settings else None, settings.longitude if settings else None, (settings.timezone if settings and settings.timezone else "UTC"))
    # Load all icons for display
    icons = {icon.name: icon for icon in Icon.query.all()}
    return render_template("display/sign.html", settings=settings, schedule=active, items=items, weather=weather, icons=icons)


@display_bp.route("/check-updates")
def check_updates():
    """Lightweight endpoint to check if settings or schedule have been updated"""
    settings = SiteSettings.query.first()
    active = Schedule.query.filter_by(is_active=True).order_by(Schedule.date.desc()).first()
    
    # Get timestamps for change detection
    settings_timestamp = settings.updated_at.isoformat() if settings and settings.updated_at else None
    schedule_timestamp = active.updated_at.isoformat() if active and active.updated_at else None
    schedule_id = active.id if active else None
    
    return jsonify({
        "settings_updated_at": settings_timestamp,
        "schedule_updated_at": schedule_timestamp,
        "schedule_id": schedule_id,
        "has_active_schedule": active is not None
    })



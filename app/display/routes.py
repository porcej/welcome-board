from flask import render_template
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



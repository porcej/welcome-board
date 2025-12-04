from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, IntegerField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, NumberRange


def get_icon_choices():
    """Get icon choices dynamically from database and built-in icons"""
    choices = [("", "None")]
    # Built-in Bootstrap icons
    builtin = [
        ("info", "Info"),
        ("star", "Star"),
        ("flag", "Flag"),
        ("calendar", "Calendar"),
        ("clock", "Clock"),
        ("bell", "Bell"),
        ("exclamation", "Exclamation"),
        ("check", "Check"),
        ("heart", "Heart"),
        ("fire", "Fire"),
        ("trophy", "Trophy"),
        ("lightning", "Lightning"),
        ("shield", "Shield")
    ]
    choices.extend(builtin)
    # Custom icons from database
    try:
        from ..models import Icon
        custom_icons = Icon.query.filter_by(enabled=True).order_by(Icon.name).all()
        for icon in custom_icons:
            choices.append((icon.name, icon.name))
    except Exception:
        pass  # Database might not be initialized yet
    return choices


class ScheduleForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    date = DateField("Date", validators=[Optional()], format="%Y-%m-%d")
    is_active = BooleanField("Active")
    show_name = BooleanField("Show Name on Display")
    submit = SubmitField("Save")


class ScheduleItemForm(FlaskForm):
    name = StringField("Name", validators=[Optional()])
    start_time = TimeField("Start Time", validators=[DataRequired()], format="%H:%M")
    duration_minutes = IntegerField("Duration (minutes)", validators=[Optional(), NumberRange(min=1, max=24 * 60)])
    location = StringField("Location", validators=[Optional()])
    uniform = StringField("Uniform", validators=[Optional()])
    lead = StringField("Lead", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])
    icon = SelectField("Icon", choices=get_icon_choices, validators=[Optional()])
    submit = SubmitField("Save")



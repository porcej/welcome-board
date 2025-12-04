from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import Optional, Regexp, NumberRange
from flask_wtf.file import FileField, FileAllowed


def get_timezone_choices():
    """Get list of common timezones for dropdown"""
    return [
        ("", "Select a timezone..."),
        ("UTC", "UTC (Coordinated Universal Time)"),
        # US Timezones
        ("America/New_York", "US Eastern Time (New York)"),
        ("America/Chicago", "US Central Time (Chicago)"),
        ("America/Denver", "US Mountain Time (Denver)"),
        ("America/Phoenix", "US Mountain Time - Arizona (Phoenix)"),
        ("America/Los_Angeles", "US Pacific Time (Los Angeles)"),
        ("America/Anchorage", "US Alaska Time (Anchorage)"),
        ("Pacific/Honolulu", "US Hawaii Time (Honolulu)"),
        # Canada
        ("America/Toronto", "Canada Eastern Time (Toronto)"),
        ("America/Vancouver", "Canada Pacific Time (Vancouver)"),
        ("America/Winnipeg", "Canada Central Time (Winnipeg)"),
        # Europe
        ("Europe/London", "UK Time (London)"),
        ("Europe/Paris", "Central European Time (Paris)"),
        ("Europe/Berlin", "Central European Time (Berlin)"),
        ("Europe/Rome", "Central European Time (Rome)"),
        ("Europe/Madrid", "Central European Time (Madrid)"),
        ("Europe/Amsterdam", "Central European Time (Amsterdam)"),
        ("Europe/Brussels", "Central European Time (Brussels)"),
        ("Europe/Vienna", "Central European Time (Vienna)"),
        ("Europe/Stockholm", "Central European Time (Stockholm)"),
        ("Europe/Warsaw", "Central European Time (Warsaw)"),
        ("Europe/Prague", "Central European Time (Prague)"),
        ("Europe/Athens", "Eastern European Time (Athens)"),
        ("Europe/Helsinki", "Eastern European Time (Helsinki)"),
        ("Europe/Moscow", "Moscow Time"),
        ("Europe/Dublin", "Ireland Time (Dublin)"),
        ("Europe/Lisbon", "Western European Time (Lisbon)"),
        # Asia
        ("Asia/Tokyo", "Japan Time (Tokyo)"),
        ("Asia/Shanghai", "China Time (Shanghai)"),
        ("Asia/Hong_Kong", "Hong Kong Time"),
        ("Asia/Singapore", "Singapore Time"),
        ("Asia/Seoul", "Korea Time (Seoul)"),
        ("Asia/Bangkok", "Thailand Time (Bangkok)"),
        ("Asia/Jakarta", "Indonesia Western Time (Jakarta)"),
        ("Asia/Manila", "Philippines Time (Manila)"),
        ("Asia/Kolkata", "India Time (Kolkata)"),
        ("Asia/Dubai", "UAE Time (Dubai)"),
        ("Asia/Riyadh", "Saudi Arabia Time (Riyadh)"),
        ("Asia/Tehran", "Iran Time (Tehran)"),
        ("Asia/Karachi", "Pakistan Time (Karachi)"),
        ("Asia/Dhaka", "Bangladesh Time (Dhaka)"),
        # Australia & Pacific
        ("Australia/Sydney", "Australia Eastern Time (Sydney)"),
        ("Australia/Melbourne", "Australia Eastern Time (Melbourne)"),
        ("Australia/Brisbane", "Australia Eastern Time (Brisbane)"),
        ("Australia/Adelaide", "Australia Central Time (Adelaide)"),
        ("Australia/Perth", "Australia Western Time (Perth)"),
        ("Australia/Darwin", "Australia Central Time (Darwin)"),
        ("Pacific/Auckland", "New Zealand Time (Auckland)"),
        ("Pacific/Fiji", "Fiji Time"),
        # South America
        ("America/Sao_Paulo", "Brazil Time (São Paulo)"),
        ("America/Buenos_Aires", "Argentina Time (Buenos Aires)"),
        ("America/Santiago", "Chile Time (Santiago)"),
        ("America/Lima", "Peru Time (Lima)"),
        ("America/Bogota", "Colombia Time (Bogotá)"),
        ("America/Mexico_City", "Mexico Time (Mexico City)"),
        # Africa
        ("Africa/Johannesburg", "South Africa Time (Johannesburg)"),
        ("Africa/Cairo", "Egypt Time (Cairo)"),
        ("Africa/Lagos", "West Africa Time (Lagos)"),
        ("Africa/Nairobi", "East Africa Time (Nairobi)"),
        ("Africa/Casablanca", "Morocco Time (Casablanca)"),
    ]


class SettingsForm(FlaskForm):
    logo = FileField("Logo", validators=[FileAllowed(["png", "jpg", "jpeg", "gif"])])
    logo_size = IntegerField("Logo Size (pixels)", validators=[Optional(), NumberRange(min=50, max=500, message="Logo size must be between 50 and 500 pixels")])
    background_image = FileField("Background Image", validators=[FileAllowed(["png", "jpg", "jpeg", "gif", "webp"])])
    background_image_size = SelectField("Background Image Size", choices=[
        ("tile", "Tile"),
        ("stretch", "Stretch"),
        ("fit", "Fit"),
        ("center", "Center")
    ], validators=[Optional()])
    notes_left_col = TextAreaField("Left Column Notes", validators=[Optional()])
    latitude = FloatField("Latitude", validators=[Optional()])
    longitude = FloatField("Longitude", validators=[Optional()])
    timezone = SelectField("Timezone", choices=get_timezone_choices, validators=[Optional()])
    bg_color = StringField("Background Color", validators=[Optional(), Regexp(r'^#[0-9A-Fa-f]{6}$', message="Must be a valid hex color (e.g., #000000)")], render_kw={"type": "color"})
    text_color = StringField("Text Color", validators=[Optional(), Regexp(r'^#[0-9A-Fa-f]{6}$', message="Must be a valid hex color (e.g., #ffffff)")], render_kw={"type": "color"})
    box_color = StringField("Side Panel Color", validators=[Optional(), Regexp(r'^#[0-9A-Fa-f]{6}$', message="Must be a valid hex color (e.g., #212529)")], render_kw={"type": "color"})
    box_opacity = FloatField("Side Panel Opacity", validators=[Optional(), NumberRange(min=0.0, max=1.0, message="Opacity must be between 0.0 and 1.0")])
    schedule_color = StringField("Schedule Box Color", validators=[Optional(), Regexp(r'^#[0-9A-Fa-f]{6}$', message="Must be a valid hex color (e.g., #212529)")], render_kw={"type": "color"})
    schedule_opacity = FloatField("Schedule Box Opacity", validators=[Optional(), NumberRange(min=0.0, max=1.0, message="Opacity must be between 0.0 and 1.0")])
    submit = SubmitField("Save Settings")



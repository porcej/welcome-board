from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import Optional, Regexp, NumberRange
from flask_wtf.file import FileField, FileAllowed


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
    timezone = StringField("Timezone", validators=[Optional()])
    bg_color = StringField("Background Color", validators=[Optional(), Regexp(r'^#[0-9A-Fa-f]{6}$', message="Must be a valid hex color (e.g., #000000)")], render_kw={"type": "color"})
    text_color = StringField("Text Color", validators=[Optional(), Regexp(r'^#[0-9A-Fa-f]{6}$', message="Must be a valid hex color (e.g., #ffffff)")], render_kw={"type": "color"})
    box_color = StringField("Side Panel Color", validators=[Optional(), Regexp(r'^#[0-9A-Fa-f]{6}$', message="Must be a valid hex color (e.g., #212529)")], render_kw={"type": "color"})
    box_opacity = FloatField("Side Panel Opacity", validators=[Optional(), NumberRange(min=0.0, max=1.0, message="Opacity must be between 0.0 and 1.0")])
    schedule_color = StringField("Schedule Box Color", validators=[Optional(), Regexp(r'^#[0-9A-Fa-f]{6}$', message="Must be a valid hex color (e.g., #212529)")], render_kw={"type": "color"})
    schedule_opacity = FloatField("Schedule Box Opacity", validators=[Optional(), NumberRange(min=0.0, max=1.0, message="Opacity must be between 0.0 and 1.0")])
    submit = SubmitField("Save Settings")



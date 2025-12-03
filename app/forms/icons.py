from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FileField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
from flask_wtf.file import FileAllowed
from ..models import Icon


class IconForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    enabled = BooleanField("Enabled", default=True)
    image = FileField("Image", validators=[FileAllowed(["png", "jpg", "jpeg", "gif", "svg", "webp"])])
    use_text = BooleanField("Use Text Instead of Image", default=False)
    characters = StringField("Characters", validators=[Optional()])
    font = SelectField("Font", choices=[
        ("Arial", "Arial"),
        ("Helvetica", "Helvetica"),
        ("Times New Roman", "Times New Roman"),
        ("Courier New", "Courier New"),
        ("Verdana", "Verdana"),
        ("Georgia", "Georgia"),
        ("Palatino", "Palatino"),
        ("Garamond", "Garamond"),
        ("Comic Sans MS", "Comic Sans MS"),
        ("Trebuchet MS", "Trebuchet MS"),
        ("Impact", "Impact"),
        ("Lucida Console", "Lucida Console"),
        ("Tahoma", "Tahoma"),
        ("Monaco", "Monaco"),
        ("Consolas", "Consolas"),
    ], validators=[Optional()])
    submit = SubmitField("Save")

    def __init__(self, *args, icon=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = icon

    def validate_name(self, field):
        if self.icon and self.icon.name == field.data:
            return  # Same icon, name unchanged
        if Icon.query.filter_by(name=field.data).first():
            raise ValidationError("An icon with this name already exists.")

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        # Must have either image or characters
        if not self.use_text.data:
            if not self.image.data and not (self.icon and self.icon.image_path):
                self.image.errors.append("Either upload an image or use text.")
                return False
        else:
            if not self.characters.data:
                self.characters.errors.append("Characters are required when using text.")
                return False
            if not self.font.data:
                self.font.errors.append("Font is required when using text.")
                return False
        return True


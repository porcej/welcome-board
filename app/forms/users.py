from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, ValidationError
from ..models import User


class UserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Optional(), Length(min=6, message="Password must be at least 6 characters")])
    is_admin = BooleanField("Admin User", default=False)
    submit = SubmitField("Save")

    def __init__(self, *args, user=None, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=field.data.lower().strip()).first()
        if existing_user and (not self.user or existing_user.id != self.user.id):
            raise ValidationError("This email is already registered.")


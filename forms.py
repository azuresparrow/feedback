from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, email_validator, ValidationError

from models import User

class RegisterUserForm(FlaskForm):
    """Form to register a new user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


    def validate_username(form, field):
        if User.username_taken(field.data):
            raise ValidationError("Username is taken")

class LoginUserForm(FlaskForm):
    """Form for a user to log in"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
"""
Stores all web form classes. Each form is passed to the appropriate web page
via the page's view function in app/routes.py.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    username= StringField("Username", validators=[DataRequired()])
    password= PasswordField("Password", validators=[DataRequired()])
    remember_me= BooleanField("Remember Me")
    submit= SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    # Each field is required. For `email`, there is a further validation that
    # the email match the format of an email address.
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    # Any method matching the the patter `validate_<field_name>` will be
    # executed as a validation. There two methods check to see if the username
    # or email already exists in the user database, raising an exception if one
    # is found.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already taken.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email already taken.")


"""
Stores all web form classes. Each form is passed to the appropriate web page
via the page's view function in app/routes.py.
"""

import flask_wtf
import wtforms as wtf
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from app.models import User


class LoginForm(flask_wtf.FlaskForm):
    username= wtf.StringField("Username", validators=[DataRequired()])
    password= wtf.PasswordField("Password", validators=[DataRequired()])
    remember_me= wtf.BooleanField("Remember Me")
    submit= wtf.SubmitField("Sign In")


class RegistrationForm(flask_wtf.FlaskForm):
    # Each field is required. For `email`, there is a further validation that
    # the email match the format of an email address.
    username = wtf.StringField("Username", validators=[DataRequired()])
    email = wtf.StringField("Email", validators=[DataRequired(), Email()])
    password = wtf.PasswordField("Password", validators=[DataRequired()])
    password2 = wtf.PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = wtf.SubmitField("Register")

    # Any method matching the the pattern `validate_<field_name>` will be
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


class EditProfileForm(flask_wtf.FlaskForm):
    username = wtf.StringField("Username", validators=[DataRequired()])
    about_me = wtf.TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = wtf.SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Please use a different username.")



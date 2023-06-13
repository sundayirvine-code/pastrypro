from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    """
    Represents a registration form.
    
    Attributes:
        username (StringField): Field for entering a username.
        email (StringField): Field for entering an email address.
        password (PasswordField): Field for entering a password.
        confirm_password (PasswordField): Field for confirming the password.
        submit (SubmitField): Button for submitting the form.
    """
    
    username = StringField('Username', validators=[DataRequired()], render_kw={"autocomplete": "off"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"autocomplete": "off"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"autocomplete": "off"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"autocomplete": "off"})
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
    Represents a login form.
    
    Attributes:
        email (StringField): Field for entering an email address.
        password (PasswordField): Field for entering a password.
        submit (SubmitField): Button for submitting the form.
    """
    
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"autocomplete": "off"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"autocomplete": "off"})
    submit = SubmitField('Log In')


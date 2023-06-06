from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"autocomplete": "off"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"autocomplete": "off"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"autocomplete": "off"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"autocomplete": "off"})
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"autocomplete": "off"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"autocomplete": "off"})
    submit = SubmitField('Log In')

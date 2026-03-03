from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email
from flask_login import current_user

import sqlalchemy as sqla
from sqlalchemy import func
from app.main.models import User
from app import db

class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    user_type = RadioField('Choose user type', choices=[('regular', 'Regular user'), ('certified', 'Certified user')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalars(sqla.select(User).where(func.lower(User.username) == username.data.lower())).first()
        if user is not None:
            # if user.id != current_user.id:
            raise ValidationError('This username already exists! Please provide a different username')
        
    def validate_email(self, email):
        user = db.session.scalars(sqla.select(User).where(User.email == email.data)).first()
        if user is not None:
            # if user.id != current_user.id:
            raise ValidationError('This email is already registered! Please provide a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

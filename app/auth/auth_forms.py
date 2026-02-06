from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email
from flask_login import current_user

import sqlalchemy as sqla
from app.main.models import User
from app import db

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    curr_ingredients = TextAreaField('Current Ingredients')

    submit = SubmitField('Register')

    def validate_username(self, username):
        query = sqla.select(User).where(User.username == username.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('This username already exists! Please provide a different username')
        
    def validate_email(self, email):
        query = sqla.select(User).where(User.email == email.data)
        user = db.session.scalars(query).first()
        if user is not None:
            if user.id != current_user.id:
                raise ValidationError('This email is already registered! Please provide a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

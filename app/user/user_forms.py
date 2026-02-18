from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, URL, ValidationError, DataRequired

from app import db
import sqlalchemy as sqla
from app.main.models import User


class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = db.session.scalars(sqla.select(User).where(User.username == username.data)).first()
        if user is not None:
            if user.id != current_user.id:
                raise ValidationError('This username is already registered! Please provide a different username.')
            
    def validate_email(self, email):
        user = db.session.scalars(sqla.select(User).where(User.email == email.data)).first()
        if user is not None:
            if user.id != current_user.id:
                raise ValidationError('This email is already registered! Please provide a different email address.')

class BusinessForm(FlaskForm):
    business_name = StringField('Business Name', validators=[DataRequired()])
    business_website = StringField('Business Website', validators=[DataRequired(), URL()])
    submit = SubmitField('Save Business Information')
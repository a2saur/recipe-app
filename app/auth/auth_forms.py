from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, PasswordField, BooleanField, FieldList, FormField, SelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from flask_login import current_user

import sqlalchemy as sqla
from app.main.models import User, Tag
from app.recipe.recipe_forms import IngredientForm
from app import db

class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    user_type = RadioField('Choose user type', choices=[('regular', 'Regular user'), ('certified', 'Certified user')], validators=[DataRequired()])
    allergies = FieldList(FormField(IngredientForm))
    dietary_restirctions = SelectMultipleField('Dietary Restrictions',
        choices=[
            ('vegan', 'Vegan'),
            ('vegetarian', 'Vegetarian'),
            ('gluten_free', 'Gluten Free'),
            ('kosher', 'Kosher')
        ],
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput())
    tags = QuerySelectMultipleField('Select Preferred Tags', query_factory = lambda : db.session.scalars(sqla.select(Tag).order_by(Tag.name)), get_label = lambda tag: tag.name,
                                    widget = ListWidget(prefix_label=False),option_widget = CheckboxInput())
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalars(sqla.select(User).where(User.username == username.data)).first()
        if user is not None:
            if user.id != current_user.id:
                raise ValidationError('This username already exists! Please provide a different username')
        
    def validate_email(self, email):
        user = db.session.scalars(sqla.select(User).where(User.email == email.data)).first()
        if user is not None:
            if user.id != current_user.id:
                raise ValidationError('This email is already registered! Please provide a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

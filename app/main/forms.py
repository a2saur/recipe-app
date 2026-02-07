from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, PasswordField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, Length
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired, EqualTo, Email

from app import db
import sqlalchemy as sqla
from app.main.models import Tag, User

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=1500)])
    servingSize = FloatField('Serving Size', validators=[DataRequired(), Length(min=1, max=1500)])
    tag = QuerySelectMultipleField('Tag', query_factory = lambda : db.session.scalars(sqla.select(Tag).order_by(Tag.name)), get_label= lambda tag: tag.name,
                                   widget = ListWidget(prefix_label=False), option_widget=CheckboxInput())
    submit = SubmitField('Post')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class SortForm(FlaskForm):
    sortby = SelectField('Sort by', choices=['Date', 'Title', "# of likes", "Happiness level"])
    my_recipes_only = BooleanField('Display my recipes only')
    refresh = SubmitField('Refresh')

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
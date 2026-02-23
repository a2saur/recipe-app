from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import Form, FormField, FieldList, StringField, SubmitField, SelectField, TextAreaField, BooleanField, PasswordField, FloatField, HiddenField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, Length
from wtforms.widgets import ListWidget, CheckboxInput, Select
from wtforms.validators import DataRequired, EqualTo, Email, Optional

from app import db
import sqlalchemy as sqla
from app.main.models import Tag, User, UNIT_OPTIONS

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class SortForm(FlaskForm):
    sortby = SelectField('Sort by', choices=['Date', "# of likes", "Certified"])
    refresh = SubmitField('Refresh')

class FilterForm(FlaskForm):
    tags = QuerySelectMultipleField('Tags', query_factory = lambda : db.session.scalars(sqla.select(Tag).order_by(Tag.name)), 
                                    get_label= lambda tag: tag.name,
                                    render_kw={"class": "form-control", "size": "1", "placeholder": "Select Tags"})
    all_selected = BooleanField('All Selected')
    certified = BooleanField('Certified Only')
    likes = StringField('Likes', render_kw={"placeholder": "Min # of Saves"})
    # date
    # likes
    # certifieduser
    refresh = SubmitField('Filter')

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

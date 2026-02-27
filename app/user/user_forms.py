from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, FieldList, FormField, Form
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.validators import DataRequired, EqualTo, Email, URL, ValidationError, DataRequired, Optional

from app import db
import sqlalchemy as sqla
from app.main.models import User, Certification
from app.recipe.recipe_forms import IngredientForm

# Standalone form
class IngredientSubmitForm(IngredientForm, FlaskForm):
    submit = SubmitField('Add Ingredient')

class CertificationForm(Form):
    certifications = QuerySelectField('Certifications', query_factory = lambda : db.session.scalars(sqla.select(Certification).order_by(Certification.name)), 
                                    get_label= lambda certification: certification.name, allow_blank=True, blank_text="Select a Certification")
    dateRecieved = DateField('Date Recieved', format = "%Y-%m-%d", validators=[Optional()])

class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    certifications = FieldList(FormField(CertificationForm), min_entries=0)
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

class CertifyForm(FlaskForm):
    in_code = StringField('One-Time Code', validators=[DataRequired()], render_kw={'placeholder':'Your code'})
    certifications = FieldList(FormField(CertificationForm), min_entries=1)
    submit = SubmitField('Certify')

class BusinessForm(FlaskForm):
    business_name = StringField('Business Name', validators=[DataRequired()])
    business_website = StringField('Business Website', validators=[DataRequired(), URL()])
    submit = SubmitField('Save Business Information')
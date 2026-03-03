from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, SubmitField, PasswordField, SelectMultipleField, DateField, FieldList, FormField, Form, FloatField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired, EqualTo, Email, URL, ValidationError, DataRequired, Optional, NumberRange

from app import db
import sqlalchemy as sqla
from app.main.models import User, Tag, Certification, UNIT_OPTIONS
from app.recipe.recipe_forms import IngredientForm

# Standalone form
class IngredientSubmitForm(IngredientForm, FlaskForm):
    submit = SubmitField('Add Ingredient')

class CertificationForm(Form):
    certifications = QuerySelectField('Certifications', query_factory = lambda : db.session.scalars(sqla.select(Certification).order_by(Certification.name)), 
                                    get_label= lambda certification: certification.name, allow_blank=True, blank_text="Select a Certification")
    dateRecieved = DateField('Date Recieved', format = "%Y-%m-%d", validators=[Optional()])

class IngredientCostForm(FlaskForm):
    ingredientName = StringField('Ingredient', validators=[DataRequired()])
    unit = SelectField('Unit', choices=UNIT_OPTIONS, default="unit")
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.0)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.0)])
    submit = SubmitField('Add')

class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    allergies = FieldList(FormField(IngredientForm))
    dietary_restrictions = QuerySelectMultipleField(
        'Special Dietary Categories', 
        query_factory=lambda: db.session.scalars(
            sqla.select(Tag)
            .where(Tag.name.in_(['vegan', 'vegetarian', 'kosher', 'pescetarian', 'kosher', 'halal', 'gluten-free']))
            .order_by(Tag.name)
        ), 
        get_label=lambda tag: tag.name,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput()
    )
    tags = QuerySelectMultipleField(
        'Select Preferred Tags', 
        query_factory=lambda: db.session.scalars(
        sqla.select(Tag)
        .where(Tag.name.notin_(['vegetarian', 'vegan', 'kosher', 'pescetarian', 'kosher', 'halal', 'gluten-free']))
        .order_by(Tag.name)
    ), get_label = lambda tag: tag.name,
    widget = ListWidget(prefix_label=False),option_widget = CheckboxInput()
    )
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

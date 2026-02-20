from flask_wtf import FlaskForm
from wtforms import Form, FormField, FieldList, StringField, SubmitField, SelectField, TextAreaField, FloatField, HiddenField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import  Length
from wtforms.validators import Optional
from flask_wtf.file import FileField

from app import db
import sqlalchemy as sqla
from app.main.models import Tag, UNIT_OPTIONS

# Subform (no CSRF)
class IngredientForm(Form):
    ingredient_id = HiddenField()
    ingredientName = StringField('Ingredient Name', default="")
    quantity = FloatField('Quantity', default=0.0, validators=[Optional()])
    unit = SelectField('Unit', choices=UNIT_OPTIONS, default="unit")

# Standalone form
class IngredientSubmitForm(IngredientForm, FlaskForm):
    submit = SubmitField('Add')

class RecipeForm(FlaskForm):
    title = StringField('Title*')
    pictFile = FileField("Picture (optional)", validators=[Optional()])
    description = TextAreaField('Description*', validators=[Length(max=215)])
    servingSize = FloatField('Serving Size*', default=0.0, validators=[Optional()])
    estimatedTime = StringField('Estimated Time*', validators=[Length(max=25)])
    tags = QuerySelectMultipleField('Tags (optional)', query_factory = lambda : db.session.scalars(sqla.select(Tag).order_by(Tag.name)), 
                                    get_label= lambda tag: tag.name,
                                    render_kw={"class": "form-control", "size": "1"})
    ingredients = FieldList(FormField(IngredientForm))
    steps = TextAreaField('Steps*')

    submit = SubmitField('Post')

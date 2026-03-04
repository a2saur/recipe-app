from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import Form, FormField, FieldList, StringField, SubmitField, SelectField, TextAreaField, BooleanField, PasswordField, FloatField, HiddenField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, Length, InputRequired
from wtforms.widgets import ListWidget, CheckboxInput, Select
from wtforms.validators import DataRequired, EqualTo, Email, Optional
from flask_wtf.file import FileField

from app import db
import sqlalchemy as sqla
from app.main.models import Tag, User, UNIT_OPTIONS, Recipe


class CookbookForm(FlaskForm):
    title = StringField('Title*', validators=[DataRequired()])
    pictFile = FileField("Cover Picture (optional)", validators=[Optional()])
    description = TextAreaField('Description*', validators=[DataRequired(), Length(max=215)])
    recipes = QuerySelectMultipleField('Recipes*', 
                                    query_factory = lambda : db.session.scalars(sqla.select(Recipe).where(Recipe.user_id == current_user.id).order_by(Recipe.title)),
                                    get_label= lambda recipe: recipe.title,
                                    render_kw={"class": "form-control", "size": "1"})
    submit = SubmitField('Post')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, Length
from wtforms.widgets import ListWidget, CheckboxInput

from app import db
import sqlalchemy as sqla
from app.main.models import Tag

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=1, max=1500)])
    tag = QuerySelectMultipleField('Tag', query_factory = lambda : db.session.scalars(sqla.select(Tag).order_by(Tag.name)), get_label= lambda tag: tag.name,
                                   widget = ListWidget(prefix_label=False), option_widget=CheckboxInput())   
    submit = SubmitField('Post')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class SortForm(FlaskForm):
    sortby = SelectField('Sort by', choices=['Date', 'Title', "# of likes", "Happiness level"])
    my_recipes_only = BooleanField('Display my recipes only')
    refresh = SubmitField('Refresh')


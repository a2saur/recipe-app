from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField, IntegerField, DateField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import Optional, NumberRange

from app import db
import sqlalchemy as sqla
from app.main.models import Tag

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class SortForm(FlaskForm):
    sortby = SelectField('Sort by', choices=['Date', "# of saves", "Certified first"])
    refresh = SubmitField('Refresh')

class FilterSortForm(FlaskForm):
    sortby = SelectField('Sort by', choices=['Date', "# of saves", "Certified first"])
    tags = QuerySelectMultipleField('Tags', query_factory = lambda : db.session.scalars(sqla.select(Tag).order_by(Tag.name)), 
                                    get_label= lambda tag: tag.name,
                                    render_kw={"class": "form-control", "size": "1", "placeholder": "Select Tags"})
    all_selected = BooleanField('All Selected')
    certified = BooleanField('Certified Only')
    saves = IntegerField('Saves', render_kw={"placeholder": "Min # of Saves"}, validators=[Optional(), NumberRange(min=0, message="Input must be positive")])
    min_date = DateField('Posted After', validators=[Optional()])
    max_cost = IntegerField('Max Cost ($)', render_kw={"placeholder": "$"}, validators = [Optional(), NumberRange(min=0, message="Input cannot be negative")])
    refresh = SubmitField('Sort / Filter')



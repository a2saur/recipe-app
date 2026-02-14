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

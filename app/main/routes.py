from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from flask_login import current_user, login_required

from app import db
from app.main.models import Recipe, RecipeIngredientUse, Ingredient, Tag, User, recipe_tags_table, UserGroceryListUse, UserIngredientListUse
from app.main.forms import RecipeForm, IngredientSubmitForm, EmptyForm, SortForm, EditForm
from app.auth.auth_forms import RegistrationForm

from app.main import main_blueprint as bp_main


@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    empty_form = EmptyForm()
    sort_form = SortForm()
    filter_form = FilterForm()
    if request.method == 'POST':
        if sort_form.validate_on_submit():
            base_query = sqla.select(Recipe).where(Recipe.is_draft == False)
            if sort_form.sortby.data == "Title":
                recipes = base_query.order_by(Recipe.title)
            else:
                recipes = base_query.order_by(Recipe.timestamp.desc())
    if request.method == 'GET':
        recipes = sqla.select(Recipe).where(Recipe.is_draft == False).order_by(Recipe.timestamp.desc())
    all_recipes  = db.session.scalars(recipes).all() 
    return render_template('index.html', title="", recipes=all_recipes, form=empty_form, sortform = sort_form)

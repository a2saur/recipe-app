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
def index(sort_data="Date"):
    empty_form = EmptyForm()
    sort_form = SortForm()
    base_query = sqla.select(Recipe).where(Recipe.is_draft == False)
    if request.method == 'POST':
        sort_data = sort_form.sortby.data
        if sort_form.validate_on_submit():
            if sort_data== "# of likes":
                recipes = base_query.order_by(Recipe.save_count.desc())
            elif sort_data == "Certified":
                recipes = base_query.join(Recipe.writer).order_by(User.is_certified.desc())
            else:
                recipes = base_query.order_by(Recipe.timestamp.desc())
    if request.method == 'GET':
            recipes = base_query.order_by(Recipe.timestamp.desc())
    all_recipes  = db.session.scalars(recipes).all() 
    return render_template('index.html', title="", recipes=all_recipes, form=empty_form, sortform = sort_form)

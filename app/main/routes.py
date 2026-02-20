from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from flask_login import current_user, login_required

from app import db
from app.main.models import Cookbook, Recipe, RecipeIngredientUse, Ingredient, Tag, User, recipe_tags_table, UserGroceryListUse, UserIngredientListUse
from app.main.forms import EmptyForm, SortForm
from app.auth.auth_forms import RegistrationForm
from app.main.helpers import get_recommended_recipes

from app.main import main_blueprint as bp_main


@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET', 'POST'])
# @login_required
def index(sort_data="Date"):
    empty_form = EmptyForm()
    sort_form = SortForm()

    rec_recipes = get_recommended_recipes(current_user.id)


    # sort by implementation
    base_query = sqla.select(Recipe).where(Recipe.is_draft == False)
    if request.method == 'POST':
        sort_data = sort_form.sortby.data
        if sort_form.validate_on_submit():
            if sort_data== "# of saves":
                recipes = base_query.order_by(Recipe.save_count.desc())
            elif sort_data == "Certified":
                recipes = base_query.join(Recipe.writer).order_by(User.is_certified.desc())
            else:
                recipes = base_query.order_by(Recipe.timestamp.desc())

    # default: order by most recent 
    if request.method == 'GET':
            recipes = base_query.order_by(Recipe.timestamp.desc())
    all_recipes  = db.session.scalars(recipes).all() 
    recipe_len = len(all_recipes)
  
    # get all cookbooks to display
    all_cookbooks  = db.session.scalars(sqla.select(Cookbook)).all()
    
    return render_template('index.html', title="", recipe_len=recipe_len, rec_recipes=rec_recipes, recipes=all_recipes, cookbooks=all_cookbooks, form=empty_form, sortform = sort_form)

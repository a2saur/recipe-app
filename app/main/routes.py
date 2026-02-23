from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from flask_login import current_user, login_required

from app import db
from app.main.models import Cookbook, Recipe, RecipeIngredientUse, Ingredient, Tag, User, recipe_tags_table, UserGroceryListUse, UserIngredientListUse
from app.main.forms import EmptyForm, FilterSortForm
from app.auth.auth_forms import RegistrationForm
from app.main.helpers import get_recommended_recipes

from app.main import main_blueprint as bp_main


@bp_main.route('/', methods=['GET', 'POST'])
@bp_main.route('/index', methods=['GET', 'POST'])
# @login_required
def index(sort_data="Date"):
    empty_form = EmptyForm()
    # get recommended recipes
    rec_recipes = get_recommended_recipes(current_user.id)
    # sort form
    fs_form = FilterSortForm()
    base_query = sqla.select(Recipe).where(Recipe.is_draft == False)
    text = ""
    if request.method == 'POST':
        if fs_form.validate_on_submit():
            tag_list = [tag.name for tag in fs_form.tags.data]
            if len(tag_list) > 0:
                if fs_form.all_selected.data:
                    for tag in tag_list:
                        base_query = base_query.filter(Recipe.tags.any(Tag.name == tag))
                else:
                    base_query = base_query.filter(Recipe.tags.any(Tag.name.in_(tag_list)))
                text = "Filters/Sorting Applied"
            if fs_form.certified.data:
                base_query = base_query.join(Recipe.writer).where(User.is_certified)
                text = "Filters/Sorting Applied"
            if fs_form.likes.data:
                base_query = base_query.where(Recipe.save_count >= fs_form.likes.data)
                text = "Filters/Sorting Applied"
            if fs_form.min_date.data:
                base_query = base_query.where(Recipe.timestamp >= fs_form.min_date.data)
                text = "Filters/Sorting Applied"
            recipes = base_query.order_by(Recipe.timestamp.desc())
            if sort_data := fs_form.sortby.data:
                text = "Filters/Sorting Applied"
                if sort_data== "# of likes":
                    recipes = base_query.order_by(Recipe.save_count.desc())
                elif sort_data == "Certified":
                    recipes = base_query.join(Recipe.writer).order_by(User.is_certified.desc())
                else:
                    recipes = base_query.order_by(Recipe.timestamp.desc())
    if request.method == 'GET':
        recipes = base_query.order_by(Recipe.timestamp.desc())
    all_recipes  = db.session.scalars(recipes).all() 

    # get all cookbooks
    all_cookbooks  = db.session.scalars(sqla.select(Cookbook)).all()

    recipe_count = len(all_recipes)

    return render_template('index.html', title="", rec_recipes=rec_recipes, recipe_count=recipe_count, recipes=all_recipes, cookbooks=all_cookbooks, form=empty_form, filterform = fs_form, filter_text=text)
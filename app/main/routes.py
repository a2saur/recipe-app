from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from flask_login import current_user, login_required

from app import db
from app.main.models import Recipe, RecipeIngredientUse, Ingredient, Tag, User, recipe_tags_table, UserGroceryListUse, UserIngredientListUse
from app.main.forms import RecipeForm, IngredientSubmitForm, EmptyForm, SortForm, EditForm, FilterForm
from app.auth.auth_forms import RegistrationForm

from app.main import main_blueprint as bp_main


@bp_main.route('/', methods=['GET', 'POST'])
@bp_main.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    empty_form = EmptyForm()
    sort_form = SortForm()
    filter_form = FilterForm()
    base_query = sqla.select(Recipe).where(Recipe.is_draft == False)
    if request.method == 'POST':
        if filter_form.validate_on_submit():
            tag_list = [tag.name for tag in filter_form.tags.data]
            if len(tag_list) > 0:
                if filter_form.all_selected.data:
                    for tag in tag_list:
                        base_query = base_query.filter(Recipe.tags.any(Tag.name == tag))
                else:
                    base_query = base_query.filter(Recipe.tags.any(Tag.name.in_(tag_list)))
            if filter_form.certified.data:
                base_query = base_query.join(Recipe.writer).where(User.is_certified)
            recipes = base_query.order_by(Recipe.timestamp.desc())
        if sort_form.validate_on_submit():
            if sort_form.sortby.data == "Title":
                recipes = base_query.order_by(Recipe.title)
            else:
                recipes = base_query.order_by(Recipe.timestamp.desc())
    if request.method == 'GET':
        recipes = base_query.order_by(Recipe.timestamp.desc())
    all_recipes  = db.session.scalars(recipes).all() 
    return render_template('index.html', title="", recipes=all_recipes, form=empty_form, sortform = sort_form, filterform = filter_form)

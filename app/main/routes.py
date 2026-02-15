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

@bp_main.route('/ingredients', methods=['GET','POST'])
# @login_required
def view_ingredients():
    iform = IngredientSubmitForm(prefix="curr")
    gform = IngredientSubmitForm(prefix="groc")

    # get the user's current ingredients 
    curr_ingredients = current_user.get_curr_ingredients()
    # get the user's grocery list ingredients
    grocery_list = current_user.get_grocery_list()
    
    if iform.submit.data and iform.validate():
        ingredient = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == iform.ingredientName.data)).first()
        if not ingredient:
            ingredient = Ingredient(name=iform.ingredientName.data)
            db.session.add(ingredient)
            db.session.commit()
        current_user.add_ingredient(ingredient, iform.quantity.data, iform.unit.data)
        return redirect(url_for('main.view_ingredients'))
    
    elif gform.submit.data and gform.validate():
        ingredient = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == gform.ingredientName.data)).first()
        if not ingredient:
            ingredient = Ingredient(name=gform.ingredientName.data)
            db.session.add(ingredient)
            db.session.commit()
        current_user.add_grocery(ingredient, gform.quantity.data, gform.unit.data)
        return redirect(url_for('main.view_ingredients'))
    return render_template('view_ingredients.html', title="Ingredients", ingredients=curr_ingredients, grocery_list=grocery_list, iform=iform, gform=gform)

@bp_main.route('/ingredients/move_or_delete_grocery', methods=['POST'])
# @login_required
def move_or_delete_grocery():
    action = request.form.get('action')
    selected_grocery_ids = request.form.getlist('grocery_ids')

    if not selected_grocery_ids:
        flash('No ingredients selected to move.')
        return redirect(url_for('main.view_ingredients'))
    
    for ing_id in selected_grocery_ids:
        grocery = db.session.scalars(sqla.select(UserGroceryListUse).where(UserGroceryListUse.user_id==current_user.id).where(UserGroceryListUse.ingredient_id==int(ing_id))).first()

        if action == "purchased":
            ingredient = db.session.get(Ingredient, int(ing_id))
            current_user.add_ingredient(ingredient, grocery.amount, grocery.unit)
            db.session.delete(grocery)
        elif action == "delete":
            db.session.delete(grocery)
    
    db.session.commit()
    if action == "move":
        flash("Selected ingredients moved to current ingredients.")
    elif action == "delete":
        flash("Selected grocery items deleted.")
    return redirect(url_for('main.view_ingredients'))

@bp_main.route('/ingredients/delete_ingredient', methods=['POST'])
# @login_required
def delete_ingredient():
    selected_ingredient_ids = request.form.getlist('ingredient_ids')
    if not selected_ingredient_ids:
        flash('No ingredients selected to delete.')
        return redirect(url_for('main.view_ingredients'))
    
    for ing_id in selected_ingredient_ids:
        ingredient = db.session.scalars(sqla.select(UserIngredientListUse).where(UserIngredientListUse.user_id==current_user.id).where(UserIngredientListUse.ingredient_id==int(ing_id))).first()
        db.session.delete(ingredient)
    db.session.commit()
    flash("Selected ingredients deleted.")
    return redirect(url_for('main.view_ingredients'))

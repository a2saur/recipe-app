from datetime import datetime, timezone
import sys

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
import sqlalchemy as sqla
from app import db
from app.main.models import User, Ingredient, UserIngredientListUse, UserGroceryListUse

from app.user.user_forms import EditForm
from app.recipe.recipe_forms import IngredientSubmitForm

from app.user import user_blueprint as bp_user


@bp_user.route('/user/profile', methods=['GET','POST'])
@login_required
def display_profile():
    return render_template('profile.html', title="User Profile", user=current_user)

@bp_user.route('/user/profile/edit', methods=['GET','POST'])
@login_required
def edit_profile():
    eform = EditForm()
    if eform.validate_on_submit():
        current_user.username = eform.username.data
        current_user.first_name = eform.first_name.data
        current_user.last_name = eform.last_name.data
        current_user.email = eform.email.data
        current_user.set_password(eform.password.data)
        db.session.add(current_user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user.display_profile'))
    elif request.method == 'GET':
        eform.username.data = current_user.username
        eform.first_name.data = current_user.first_name
        eform.last_name.data = current_user.last_name
        eform.email.data = current_user.email
    return render_template('edit_profile.html', title="Edit Profile", form=eform, user=current_user)

@bp_user.route('/user/profile/certify', methods=['GET'])
@login_required
def become_certified():
    current_user.is_certified = True
    db.session.commit()
    return redirect(url_for('user.display_profile'))

@bp_user.route('/user/<recipe_id>/saverecipe', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    return

@bp_user.route('/user/<recipe_id>/removerecipe', methods=['POST'])
@login_required
def remove_saved_recipe(recipe_id):
    return

@bp_user.route('/user/ingredients', methods=['GET','POST'])
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
        return redirect(url_for('user.view_ingredients'))
    
    elif gform.submit.data and gform.validate():
        ingredient = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == gform.ingredientName.data)).first()
        if not ingredient:
            ingredient = Ingredient(name=gform.ingredientName.data)
            db.session.add(ingredient)
            db.session.commit()
        current_user.add_grocery(ingredient, gform.quantity.data, gform.unit.data)
        return redirect(url_for('user.view_ingredients'))
    return render_template('view_ingredients.html', title="Ingredients", ingredients=curr_ingredients, grocery_list=grocery_list, iform=iform, gform=gform)

@bp_user.route('/user/move_or_delete_grocery', methods=['POST'])
# @login_required
def move_or_delete_grocery():
    action = request.form.get('action')
    selected_grocery_ids = request.form.getlist('grocery_ids')

    if not selected_grocery_ids:
        flash('No ingredients selected to move.')
        return redirect(url_for('user.view_ingredients'))
    
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
    return redirect(url_for('user.view_ingredients'))

@bp_user.route('/user/delete_ingredient', methods=['POST'])
# @login_required
def delete_ingredient():
    selected_ingredient_ids = request.form.getlist('ingredient_ids')
    if not selected_ingredient_ids:
        flash('No ingredients selected to delete.')
        return redirect(url_for('user.view_ingredients'))
    
    for ing_id in selected_ingredient_ids:
        ingredient = db.session.scalars(sqla.select(UserIngredientListUse).where(UserIngredientListUse.user_id==current_user.id).where(UserIngredientListUse.ingredient_id==int(ing_id))).first()
        db.session.delete(ingredient)
    db.session.commit()
    flash("Selected ingredients deleted.")
    return redirect(url_for('user.view_ingredients'))

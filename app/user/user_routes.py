from datetime import datetime, timezone
import sys

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
import sqlalchemy as sqla
from app import db
from app.main.models import RecipeIngredientUse, User, Ingredient, UserIngredientListUse, UserGroceryListUse, Recipe, saved_recipes_table

from app.user.user_forms import EditForm, BusinessForm
from app.recipe.recipe_forms import IngredientSubmitForm

from app.user import user_blueprint as bp_user


@bp_user.route('/user/profile', methods=['GET','POST'])
@login_required
def display_profile():
    recipes=0
    cookbooks=0
    view = request.args.get('view', default = 'mine')
    if view =='mine':
        recipes = current_user.get_user_recipes()
    elif view == 'cookbook':
        cookbooks = current_user.get_user_cookbooks()
    else:
        recipes = current_user.get_saved()
    return render_template('profile.html', title="User Profile", user=current_user, recipes=recipes, cookbooks=cookbooks, view=view, read_only=False)

@bp_user.route('/user/<user_id>/viewprofile', methods = ['GET'])
@login_required
def view_other_profile(user_id):
    user=db.session.get(User, user_id)
    if user is None:
        flash("User not found")
        return redirect(url_for('main.index'))
    if user.id==current_user.id:
        return redirect(url_for('user.display_profile'))
    recipes = user.get_user_recipes()
    return render_template('profile.html', title="{user.username}'s Profile", user=user, recipes=recipes, view='mine', read_only=True)


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

@bp_user.route('/user/profile/business', methods = ['GET', 'POST'])
@login_required
def add_business():
    if not current_user.is_certified:
        flash('You must be a certified user to add a business')
        return redirect(url_for('user.display_profile'))
    bform = BusinessForm()
    if bform.validate_on_submit():
        current_user.business_name = bform.business_name.data
        current_user.business_website = bform.business_website.data
        db.session.commit()
        flash('Your Business has been added!')
        return redirect(url_for('user.display_profile'))
    return render_template('business_form.html', title="Add Business Information", form=bform, form_action='user.add_business', edit=False)

@bp_user.route('/user/profile/business/edit', methods = ['GET', 'POST'])
@login_required
def edit_business():
    if not current_user.is_certified:
        flash('You must be a certified user to add a business')
        return redirect(url_for('user.display_profile'))
    bform = BusinessForm()
    if request.method == 'GET':
        bform.business_name.data = current_user.business_name
        bform.business_website.data = current_user.business_website

    if 'delete_business' in request.form:
        current_user.business_name = None
        current_user.business_website = None
        db.session.commit()
        flash('Business Information was Deleted')
        return redirect(url_for('user.display_profile'))
    
    if bform.validate_on_submit():
        current_user.business_name = bform.business_name.data
        current_user.business_website = bform.business_website.data
        db.session.commit()
        flash('Your Business has been updated!')
        return redirect(url_for('user.display_profile'))
    return render_template('business_form.html', title="Edit Business", form=bform, form_action='user.edit_business', edit=True)

@bp_user.route('/user/<recipe_id>/saverecipe', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    theRecipe = db.session.get(Recipe, recipe_id)
    is_saved = theRecipe in current_user.get_saved()
    if is_saved:
        flash('You have already saved this recipe!')
    else:
        current_user.saved_recipes.add(theRecipe)
        db.session.commit()
        theRecipe.save_count += 1
        db.session.commit()

        # save the ingredients of the recipe to the user's grocery list
        selected_ids = request.form.getlist("ingredient_ids")

        for ing_id in selected_ids:
            ingredient = db.session.get(Ingredient, ing_id)
            recipe_ing = db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.ingredient_id == ing_id).where(RecipeIngredientUse.recipe_id == recipe_id)).first()
        
            current_user.add_grocery(
                ingredient,
                recipe_ing.amount,
                recipe_ing.unit
            )

    db.session.commit()
    flash("Recipe saved and selected ingredients added to grocery list.")
    return redirect(url_for('recipe.view_recipe', recipe_id=recipe_id))


    if request.referrer is not None:
        return redirect(request.referrer)
    else:
        return redirect(url_for('main.index'))

@bp_user.route('/user/<recipe_id>/removerecipe', methods=['POST'])
@login_required
def remove_saved_recipe(recipe_id):
    theRecipe = db.session.get(Recipe, recipe_id)
    is_saved = theRecipe in current_user.get_saved()
    if not is_saved:
        flash("You haven't saved this recipe yet!")
    else:
        current_user.saved_recipes.remove(theRecipe)
        db.session.commit()
        theRecipe.save_count -= 1
        db.session.commit()

    if request.referrer is not None:
        return redirect(request.referrer)
    else:
        return redirect(url_for('main.index'))

@bp_user.route('/user/ingredients', methods=['GET','POST'])
@login_required
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


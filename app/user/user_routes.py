from datetime import datetime, timezone
import sys
import secrets
from app import user
from flask import current_app
from functools import wraps

from flask import render_template, flash, redirect, url_for, request, jsonify, session
from flask_login import current_user, login_required
import sqlalchemy as sqla
from app import db
from app.main.models import RecipeIngredientUse, Tag, User, Ingredient, UserIngredientListUse, UserGroceryListUse, Recipe, saved_recipes_table, user_preferred_tags, user_allergies, user_dietary_tags, IngredientCostEntry
from app.user.user_forms import EditForm, IngredientCostForm
from app.user.user_forms import IngredientSubmitForm

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
    view=request.args.get('view', default='mine')
    user=db.session.get(User, user_id)
    if user is None:
        flash("User not found")
        return redirect(url_for('main.index'))
    if user.id==current_user.id:
        return redirect(url_for('user.display_profile', view=view))
    recipes=0
    cookbooks=0
    if view=='mine':
        recipes = user.get_user_recipes()
    elif view=='cookbook':
        cookbooks = user.get_user_cookbooks()
    recipes = user.get_user_recipes()
    return render_template('profile.html', title="{user.username}'s Profile", user=user, recipes=recipes, cookbooks=cookbooks, view=view, read_only=True)


@bp_user.route('/user/profile/edit', methods=['GET','POST'])
@login_required
def edit_profile():
    eform = EditForm()
    if eform.validate_on_submit():
        db.session.execute(user_allergies.delete().where(user_allergies.c.user_id == current_user.id))
        db.session.execute(user_dietary_tags.delete().where(user_dietary_tags.c.user_id == current_user.id))
        db.session.execute(user_preferred_tags.delete().where(user_preferred_tags.c.user_id == current_user.id))
        
        current_user.username = eform.username.data
        current_user.first_name = eform.first_name.data
        current_user.last_name = eform.last_name.data
        db.session.add(current_user)

        # add allergies
        if eform.allergies.data:
            for allergy in eform.allergies.data:
                ing_name = allergy.get('ingredientName').lower()
                if not ing_name:
                    continue
                
                ingredient = db.session.scalar(sqla.select(Ingredient).where(Ingredient.name == ing_name))

                if not ingredient:
                    ingredient = Ingredient(name=ing_name)
                    db.session.add(ingredient)
                    db.session.flush() # flush to get the ingredient id

                allergy = db.session.get(Ingredient, ingredient.id)
                current_user.allergies.add(allergy)

        # add all the preferred tags
        if eform.tags.data:
            for tag in eform.tags.data:
                tag = db.session.get(Tag, tag.id)
                current_user.preferred_tags.add(tag)
                

        # add all the dietary restriction tags
        if eform.dietary_restrictions.data:
            for tag in eform.dietary_restrictions.data:
                tag = db.session.get(Tag, tag.id)
                current_user.dietary_tags.add(tag)
    
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user.display_profile'))
    elif request.method == 'GET':
        for allergy in current_user.get_user_allergies():
            eform.allergies.append_entry({'ingredientName': allergy.name})            
        if not eform.allergies:
            eform.allergies.append_entry()
        eform.username.data = current_user.username
        eform.first_name.data = current_user.first_name
        eform.last_name.data = current_user.last_name
        eform.dietary_restrictions.data = current_user.get_dietary_tags()
        eform.tags.data = current_user.get_preferred_tags()
    return render_template('edit_profile.html', title="Edit Profile", form=eform, user=current_user)

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
    flash("Recipe saved!")
    return redirect(url_for('recipe.view_recipe', recipe_id=recipe_id))

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
        ingredient = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == iform.ingredientName.data.lower())).first()
        if not ingredient:
            if iform.ingredientName.data == "":
                flash("Error: No ingredient name")
                return redirect(url_for('user.view_ingredients'))
            else:
                ingredient = Ingredient(name=iform.ingredientName.data.lower())
                db.session.add(ingredient)
                db.session.commit()
        if iform.quantity.data <= 0:
            flash("Error: Invalid ingredient quantity")
            return redirect(url_for('user.view_ingredients'))
        current_user.add_ingredient(ingredient, iform.quantity.data, iform.unit.data)
        return redirect(url_for('user.view_ingredients'))
    
    elif gform.submit.data and gform.validate():
        ingredient = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == gform.ingredientName.data.lower())).first()
        if not ingredient:
            ingredient = Ingredient(name=gform.ingredientName.data.lower())
            db.session.add(ingredient)
            db.session.commit()
        current_user.add_grocery(ingredient, gform.quantity.data, gform.unit.data)
        return redirect(url_for('user.view_ingredients'))
    return render_template('view_ingredients.html', title="Ingredients", ingredients=curr_ingredients, grocery_list=grocery_list, iform=iform, gform=gform)

@bp_user.route('/user/move_or_delete_grocery', methods=['POST'])
@login_required
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
    if action == "purchased":
        flash("Selected ingredients moved to current ingredients.")
    elif action == "delete":
        flash("Selected grocery items deleted.")
    return redirect(url_for('user.view_ingredients'))

@bp_user.route('/user/delete_ingredient', methods=['POST'])
@login_required
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

@bp_user.route('/user/ingredientinfo', methods=['GET', 'POST'])
@login_required
def ingredient_info():
    # TODO option to only use user's entries
    iform = IngredientCostForm()
    if iform.validate_on_submit():
        # Get the ingredient the user is trying to write an entry for
        ingredientEntry = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == iform.ingredientName.data.lower())).first()
        # if no ingredient, add it
        if ingredientEntry is None:
            print("new ingredient")
            ingredientEntry = Ingredient(name = iform.ingredientName.data.lower())
            db.session.add(ingredientEntry)
            db.session.commit()
        else:
            # check if user already has entry for this
            ingredientCostEntry = db.session.scalars(sqla.select(IngredientCostEntry).where(IngredientCostEntry.user_id == current_user.id).where(IngredientCostEntry.ingredient_id == ingredientEntry.id)).first()
            # if they do, remove it
            if ingredientCostEntry is not None:
                print("replacing ingredient entry")
                db.session.delete(ingredientCostEntry)
        
        # write cost entry to db
        ingredientCostEntry = IngredientCostEntry(
            user_id = current_user.id,
            ingredient_id = ingredientEntry.id,
            cost = iform.price.data,
            amount = iform.amount.data,
            unit = iform.unit.data
        )
        db.session.add(ingredientCostEntry)
        db.session.commit()
        return redirect(url_for('user.ingredient_info'))
    else:
        if iform.errors:
            if iform.price.data <= 0:
                flash("Ingredient price must be greater than 0")
            elif iform.amount.data <= 0:
                flash("Ingredient amount must be greater than 0")
        # iform.ingredient.choices = [i.name for i in db.session.scalars(sqla.select(Ingredient).order_by(Ingredient.name)).all()]
        ingredientNames = db.session.scalars(sqla.select(Ingredient.name)).all()
        # s = sqla.select(Ingredient).join(IngredientCostEntry, Ingredient.id == IngredientCostEntry.ingredient_id).distinct().order_by(Ingredient.name)
        # ingredients = db.session.scalars(s).all()

        ingCostEntries = db.session.scalars(sqla.select(IngredientCostEntry)).all()
        ingIds = [i.ingredient_id for i in ingCostEntries]
        ingredients = db.session.query(Ingredient).filter(Ingredient.id.in_(ingIds)).order_by(Ingredient.name).all()
        print("---", current_user.global_costs)
        return render_template("ingredient_info.html", ingredientNames=ingredientNames, ingredients=ingredients, iform=iform)

@bp_user.route('/user/changecostpref', methods=['POST'])
@login_required
def change_cost_preference():
    current_user.global_costs = not current_user.global_costs
    db.session.commit()
    return redirect(url_for('user.ingredient_info'))
from datetime import datetime, timezone
import sys
from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from flask_login import current_user, login_required

from app import db
from app.main.models import Recipe, RecipeIngredientUse, Ingredient, Tag, User, recipe_tags_table
from app.main.forms import RecipeForm, IngredientForm, EmptyForm, SortForm, EditForm
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
            if sort_form.my_recipes_only.data:
                base_query = current_user.get_user_recipes_query()
            else:
                base_query = sqla.select(Recipe)

            if sort_form.sortby.data == '# of likes':
                recipes = base_query.order_by(Recipe.saves.desc())
            elif sort_form.sortby.data == "Title":
                recipes = base_query.order_by(Recipe.title)
            elif sort_form.sortby.data == "Happiness level":
                recipes = base_query.order_by(Recipe.happiness_level.desc())
            else:
                recipes = base_query.order_by(Recipe.timestamp.desc())
    if request.method == 'GET':
        recipes = sqla.select(Recipe).order_by(Recipe.timestamp.desc())
    all_recipes  = db.session.scalars(recipes).all() 
    return render_template('index.html', title="", recipes=all_recipes, form=empty_form, sortform = sort_form)


@bp_main.route('/recipe/create', methods=['GET'])
# @login_required
def createRecipe():
    # get recipe draft
    recipeDraft = current_user.get_drafted_recipe()
    print(recipeDraft)
    if recipeDraft is None:
        # make new recipe
        recipeDraft = Recipe(
            is_draft=True,
            user_id=current_user.id
        )
        db.session.add(recipeDraft)
        db.session.commit()
    
    return redirect(url_for('main.editRecipe', recipe_id=recipeDraft.id))


def saveRecipeDraft(recipe_id, rform):
    recipeDraft = db.session.get(Recipe, recipe_id)
    recipeDraft.title = rform.title.data
    recipeDraft.description = rform.description.data
    recipeDraft.servingSize = rform.servingSize.data
    recipeDraft.estimatedTime = rform.estimatedTime.data
    recipeDraft.steps = rform.steps.data
    recipeDraft.timestamp = datetime.now(timezone.utc)
    db.session.commit()

    for ingredientRel in rform.ingredients:
        if ingredientRel.ingredientName.data != "":
            print("Adding ingredient ", ingredientRel.ingredientName.data)
            # get ingredient id if there already is an ingredient
            ingredientItem = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == ingredientRel.ingredientName.data)).first()
            if ingredientItem is None:
                print("ingredient doesn't exist")
                # ingredient doesn't exist, so add it
                ingredientItem = Ingredient(name=ingredientRel.ingredientName.data)
                db.session.add(ingredientItem)
                db.session.commit()

                newIngredientUse = RecipeIngredientUse(
                    recipe_id = recipe_id,
                    ingredient_id = ingredientItem.id,
                    amount = ingredientRel.quantity.data,
                    unit = ingredientRel.unit.data
                )
                db.session.add(newIngredientUse)
                db.session.commit()
            else:
                print("ingredient exists")
                # ingredient exists, check if recipe ingredient use is already in db
                ingredientUse = db.session.get(RecipeIngredientUse, (recipe_id, ingredientItem.id))
                if ingredientUse is None:
                    print("not in db, adding")
                    # isn't in db yet, so add it
                    newIngredientUse = RecipeIngredientUse(
                        recipe_id = recipe_id,
                        ingredient_id = ingredientItem.id,
                        amount = ingredientRel.quantity.data,
                        unit = ingredientRel.unit.data
                    )
                    db.session.add(newIngredientUse)
                    db.session.commit()
                else:
                    print("in db, updating")
                    # in db, update values
                    ingredientUse.amount = ingredientRel.quantity.data
                    ingredientUse.unit = ingredientRel.unit.data
                    db.session.commit()
                    print(ingredientUse)

def removeIngredient(recipe_id, ingredient_id):
    ingredientToRemove = db.session.get(RecipeIngredientUse, (recipe_id, ingredient_id))
    if ingredientToRemove is None:
        flash("Error! Could not find ingredient in recipe")
    else:
        # Delete ingredient
        db.session.delete(ingredientToRemove)
        db.session.commit()
        flash("Successfully removed ingredient")

@bp_main.route('/recipe/<recipe_id>/edit', methods=['GET', 'POST'])
# @login_required
def editRecipe(recipe_id):
    recipeDraft = db.session.get(Recipe, recipe_id)

    ingredient_data = []
    for ingUseCase in db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == recipe_id)).all():
        ingredient_data.append({
            "ingredientName": ingUseCase.recipe_usecase_ingredients.name,
            "quantity": ingUseCase.amount,
            "unit": ingUseCase.unit,
            "ingredient_id": ingUseCase.ingredient_id
        })
    # add empty ingredient
    ingredient_data.append({
        "ingredientName": "",
        "quantity": 0.0,
        "unit": "",
    })

    if request.method == "GET":
        rform = RecipeForm(
            title = recipeDraft.title,
            description = recipeDraft.description,
            servingSize = recipeDraft.servingSize,
            estimatedTime = recipeDraft.estimatedTime,
            tags = recipeDraft.get_tags(),
            ingredients = ingredient_data,
            steps = recipeDraft.steps
        )
    else:
        rform = RecipeForm()

    print("AAAAAA")
    if rform.validate_on_submit():
        print("bbbb")
        buttonVal = request.form.get('action_button')
        print(buttonVal)
        if buttonVal == "post":
            # post recipe
            saveRecipeDraft(recipe_id=recipe_id, rform=rform)
            newRecipe = db.session.get(Recipe, recipe_id)
            newRecipe.is_draft = False
            db.session.commit()
            return redirect(url_for('main.index'))
        elif buttonVal == "add":
            # add ingredient (save draft)
            saveRecipeDraft(recipe_id=recipe_id, rform=rform)
            return redirect(url_for('main.editRecipe', recipe_id=recipe_id))
        elif buttonVal == "save":
            # save draft + return to main
            saveRecipeDraft(recipe_id=recipe_id, rform=rform)
            return redirect(url_for('main.index'))
        else:
            print("Removing ingredient")
            try:
                # remove ingredient
                buttonVal = int(buttonVal)
                saveRecipeDraft(recipe_id=recipe_id, rform=rform)
                removeIngredient(recipe_id=recipe_id, ingredient_id=buttonVal)
            except ValueError:
                # blank value
                pass
            return redirect(url_for('main.editRecipe', recipe_id=recipe_id))
    elif request.method == "POST":
        print(rform.errors)
    return render_template('create_recipe.html', title="", form=rform, recipe_id=recipe_id)


# MODIFY THIS METHOD
# @bp_main.route('/recipe/<recipe_id>/like', methods=['POST', 'GET'])
# @login_required
# def like(recipe_id):
#     recipe = db.session.get(Recipe, recipe_id)

#     if recipe is None:
#         return redirect(url_for('main.index'))
    
#     recipe.likes+=1
#     db.session.commit()
#     # re-read the Recipe object from the database to get the updated object
#     recipe = db.session.get(Recipe, recipe_id)

#     data = {'recipe_id': recipe.id, 'like_count': recipe.likes}

#     return jsonify(data)
    

@bp_main.route('/recipe/<recipe_id>/delete', methods=['POST'])
# @login_required
def delete(recipe_id):
    therecipe = db.session.scalars(sqla.select(Recipe).where(Recipe.id == recipe_id)).first()
    if therecipe is not None:
        for t in therecipe.get_tags():
            therecipe.tags.remove(t)
        db.session.commit()
        db.session.delete(therecipe)
        db.session.commit()
        flash('The recipe {} has been successfully deleted'.format(therecipe.title))
        return redirect(url_for('main.index'))
    
@bp_main.route('/user/profile', methods=['GET','POST'])
# @login_required
def display_profile():
    return render_template('profile.html', title="User Profile", user=current_user)

@bp_main.route('/user/profile/edit', methods=['GET','POST'])
# @login_required
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
        return redirect(url_for('main.display_profile'))
    elif request.method == 'GET':
        eform.username.data = current_user.username
        eform.first_name.data = current_user.first_name
        eform.last_name.data = current_user.last_name
        eform.email.data = current_user.email
    return render_template('edit_profile.html', title="Edit Profile", form=eform, user=current_user)

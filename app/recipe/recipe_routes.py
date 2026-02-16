from datetime import datetime, timezone

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
import sqlalchemy as sqla
from app import db

from app.main.models import Recipe, RecipeIngredientUse, Ingredient
from app.recipe.recipe_forms import RecipeForm
from app.recipe.recipe_helpers import *

from app.recipe import recipe_blueprint as bp_recipe

@bp_recipe.route('/recipe/<recipe_id>/view', methods=['GET'])
# @login_required
def view_recipe(recipe_id):
    theRecipe = db.session.scalars(sqla.select(Recipe).where(Recipe.id == recipe_id)).first()
    if not (theRecipe is None):
        theIngredients = db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == recipe_id)).all()
        return render_template('view_recipe.html', recipe = theRecipe, ingredients = theIngredients, img_path=os.path.join("img/recipe-imgs", theRecipe.pictFile))
    return redirect(url_for('main.index'))


@bp_recipe.route('/recipe/create', methods=['GET', 'POST'])
@login_required
# create_recipe shows the current recipe drafts and the option to create a new one
# the user will select one of these options and the system will redirect correspondingly
def create_recipe():
    # get recipe drafts
    if request.method == "GET":
        recipeDrafts = current_user.get_drafted_recipes()
        return render_template('select_recipe_to_edit.html', recipeOpts=recipeDrafts)
    else:
        # check if deleting a recipe
        buttonVal = request.form.get('remove_button')
        print("Remove:", buttonVal)
        if buttonVal is None:
            # check which recipe was selected or if it was the create new recipe option
            buttonVal = request.form.get('select_button')
            print("Select:", buttonVal)
            if buttonVal == "new":
                # new recipe
                recipeDraft = Recipe(
                    is_draft=True,
                    user_id=current_user.id
                )
                db.session.add(recipeDraft)
                db.session.commit()
                return redirect(url_for('recipe.edit_recipe', recipe_id=recipeDraft.id))
            else:
                # old recipe
                return redirect(url_for('recipe.edit_recipe', recipe_id=int(buttonVal)))
        else:
            # delete recipe
            deleteRecipe(recipe_id=int(buttonVal))
            return redirect(url_for('recipe.create_recipe'))


@bp_recipe.route('/recipe/<recipe_id>/edit', methods=['GET', 'POST'])
# @login_required
def edit_recipe(recipe_id):
    # get the associated recipe draft
    recipeDraft = db.session.get(Recipe, recipe_id)

    if request.method == "GET":
        # pre-fill the recipe draft data
        # populate ingredient forms
        ingredient_data = []
        for ingUseCase in db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == recipe_id)).all():
            ingredient_data.append({
                "ingredientName": ingUseCase.recipe_usecase_ingredient.name.capitalize(),
                "quantity": ingUseCase.amount,
                "unit": ingUseCase.unit,
                "ingredient_id": ingUseCase.ingredient_id
            })
        # add an extra empty ingredient form for a new ingredient
        ingredient_data.append({
            "ingredientName": "",
            "quantity": 0.0,
            "unit": "",
        })
        # populate recipe form
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
        # if recipe is being submitted, just get the form
        rform = RecipeForm()
    if rform.validate_on_submit():
        buttonVal = request.form.get('action_button') # get which button was pressed
        if buttonVal == "post":
            # post recipe
            # save uploaded image filename
            picture = request.files['pictFile']
            pictName = str(uuid.uuid1()) + "_" + secure_filename(picture.filename)
            # save changes
            saveRecipeDraft(recipe_id=recipe_id, rform=rform, pictFilePath=pictName)
            errors = validateRecipeDraftForPost(recipe_id)
            # validate recipe draft, check that there are no errors
            if len(errors) == 0:
                # change recipe from draft in db (ie publish it)
                newRecipe = db.session.get(Recipe, recipe_id)
                newRecipe.is_draft = False
                db.session.commit()

                # save uploaded image
                basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static/img/recipe-imgs')
                img_path = os.path.join(basedir, pictName)
                print(img_path)
                picture.save(img_path)

                # redirect to main
                return redirect(url_for('main.index'))
            else:
                # show first error
                flash('Error posting draft: {}'.format(errors[0]))
        elif buttonVal == "add":
            # add ingredient

            # save changes
            saveRecipeDraft(recipe_id=recipe_id, rform=rform)

            # redirect back to the edit recipe page
            return redirect(url_for('recipe.edit_recipe', recipe_id=recipe_id))
        elif buttonVal == "save":
            # save changes + return to main
            saveRecipeDraft(recipe_id=recipe_id, rform=rform)
            return redirect(url_for('main.index'))
        else:
            try:
                # remove ingredient
                buttonVal = int(buttonVal)

                # save changes
                saveRecipeDraft(recipe_id=recipe_id, rform=rform)

                # remove ingredient
                if recipeDraft.is_draft: # if recipe is posted, make sure there's still one ingredient
                    removeIngredient(recipe_id=recipe_id, ingredient_id=buttonVal)
                else:
                    if len(db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == recipe_id)).all()):
                        flash("Error: Need at least one ingredient on a posted recipe")
            except ValueError:
                # blank value, don't do anything
                pass

            # redirect back to the edit recipe page
            return redirect(url_for('recipe.edit_recipe', recipe_id=recipe_id))
    if recipeDraft.is_draft:
        return render_template('create_recipe.html', title="Create New Recipe", form=rform, recipe_id=recipe_id, is_draft=True)
    else:
        return render_template('create_recipe.html', title="Edit Recipe", form=rform, recipe_id=recipe_id, is_draft=False)

@bp_recipe.route('/recipe/<recipe_id>/delete', methods=['POST'])
# @login_required
def delete(recipe_id):
    result = deleteRecipe(recipe_id)
    if result:
        flash('Recipe has been successfully deleted')
    else:
        flash('Error: recipe failed to delete')
    return redirect(url_for('main.index'))
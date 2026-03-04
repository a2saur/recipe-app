from datetime import datetime, timezone

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
import sqlalchemy as sqla
from app import db

from app.main.models import Recipe, RecipeIngredientUse, Ingredient, RecipeStep
from app.recipe.recipe_forms import RecipeForm
from app.recipe.recipe_helpers import *

from app.recipe import recipe_blueprint as bp_recipe

@bp_recipe.route('/recipe/<recipe_id>/view', methods=['GET'])
# @login_required
def view_recipe(recipe_id):
    theRecipe = db.session.scalars(sqla.select(Recipe).where(Recipe.id == recipe_id)).first()
    if not (theRecipe is None):
        theIngredients = db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == recipe_id)).all()
        return render_template('view_recipe.html', recipe = theRecipe, ingredients = theIngredients)
    flash("Error: could not find recipe")
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
@login_required
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
        
        # populate stepss
        step_data = []
        for step in recipeDraft.get_steps():
            step_data.append({
                "stepDescription": step.description,
                "step_id": step.id
            })
        # add an extra empty step form for a new step
        step_data.append({
            "stepDescription":"",
        })

        # populate recipe form
        rform = RecipeForm(
            title = recipeDraft.title,
            description = recipeDraft.description,
            servingSize = recipeDraft.servingSize,
            estimatedHrs = recipeDraft.estimatedHrs,
            estimatedMins = recipeDraft.estimatedMins,
            tags = recipeDraft.get_tags(),
            ingredients = ingredient_data,
            steps = step_data
        )

    else:
        # if recipe is being submitted, just get the form
        rform = RecipeForm()
    if rform.validate_on_submit():
        buttonVal = request.form.get('action_button') # get which button was pressed
        if buttonVal is None:
            # some other button was pressed
            buttonVal = request.form.get('step_up_button')
            if buttonVal is None:
                # other button
                buttonVal = request.form.get('step_down_button') # get which button was pressed
                if buttonVal is None:
                    # remove step
                    buttonVal = request.form.get('step_remove_button') # get which button was pressed
                    try:
                        stepObj = db.session.get(RecipeStep, int(buttonVal))
                        recipeDraft.recipe_steps.remove(stepObj)
                        db.session.delete(stepObj)
                        db.session.commit()
                    except ValueError:
                        # tried to remove the only step
                        pass
                else:
                    # move step down
                    stepObj = db.session.get(RecipeStep, int(buttonVal))
                    nextStepObj = db.session.scalars(sqla.select(RecipeStep).where(RecipeStep.recipe_id == stepObj.recipe_id).where(RecipeStep.stepNum == stepObj.stepNum+1)).first()
                    if nextStepObj is None or stepObj is None:
                        flash("Couldn't reorder steps")
                    else:
                        stepObj.stepNum += 1
                        nextStepObj.stepNum -= 1
                        db.session.commit()
            else:
                # move step up
                stepObj = db.session.get(RecipeStep, int(buttonVal))
                prevStepObj = db.session.scalars(sqla.select(RecipeStep).where(RecipeStep.recipe_id == stepObj.recipe_id).where(RecipeStep.stepNum == stepObj.stepNum-1)).first()
                if prevStepObj is None or stepObj is None:
                    flash("Couldn't reorder steps")
                else:
                    stepObj.stepNum -= 1
                    prevStepObj.stepNum += 1
                    db.session.commit()
            return redirect(url_for('recipe.edit_recipe', recipe_id=recipe_id))
        elif buttonVal == "post":
            # post recipe
            # save changes
            saveRecipeDraft(recipe_id=recipe_id, rform=rform, picture=request.files['pictFile'])
            errors = validateRecipeDraftForPost(recipe_id)
            # validate recipe draft, check that there are no errors
            if len(errors) == 0:
                # change recipe from draft in db (ie publish it)
                newRecipe = db.session.get(Recipe, recipe_id)
                newRecipe.is_draft = False
                db.session.commit()

                # redirect to main
                return redirect(url_for('main.index'))
            else:
                # show first error
                flash('Error posting draft: {}'.format(errors[0]))
        elif buttonVal == "add":
            # add ingredient or step
            # save changes
            saveRecipeDraft(recipe_id=recipe_id, rform=rform, picture=request.files['pictFile'])
            # redirect back to the edit recipe page
            return redirect(url_for('recipe.edit_recipe', recipe_id=recipe_id))
        elif buttonVal == "save":
            # save changes + return to main
            saveRecipeDraft(recipe_id=recipe_id, rform=rform, picture=request.files['pictFile'])
            return redirect(url_for('main.index'))
        else:
            try:
                # remove ingredient
                buttonVal = int(buttonVal)

                # save changes
                saveRecipeDraft(recipe_id=recipe_id, rform=rform, picture=request.files['pictFile'])

                # remove ingredient
                if recipeDraft.is_draft: # if recipe is posted, make sure there's still one ingredient
                    removeIngredient(recipe_id=recipe_id, ingredient_id=buttonVal)
                else:
                    if len(db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == recipe_id)).all()) <= 1:
                        flash("Error: Need at least one ingredient on a posted recipe")
                    else:
                        removeIngredient(recipe_id=recipe_id, ingredient_id=buttonVal)
            except ValueError:
                # blank value, don't do anything
                pass

            # redirect back to the edit recipe page
            return redirect(url_for('recipe.edit_recipe', recipe_id=recipe_id))
    if recipeDraft.is_draft:
        return render_template('create_recipe.html', title="Create New Recipe", form=rform, recipe_id=recipe_id, is_draft=True, pictFile=recipeDraft.get_pict_path())
    else:
        return render_template('create_recipe.html', title="Edit Recipe", form=rform, recipe_id=recipe_id, is_draft=False, pictFile=recipeDraft.get_pict_path())

@bp_recipe.route('/recipe/<recipe_id>/delete', methods=['POST'])
# @login_required
def delete(recipe_id):
    result = deleteRecipe(recipe_id)
    if result:
        flash('Recipe has been successfully deleted')
    else:
        flash('Error: recipe failed to delete')
    return redirect(url_for('main.index'))



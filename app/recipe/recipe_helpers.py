from datetime import datetime, timezone

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
import sqlalchemy as sqla
from app import db

from app.main.models import Recipe, RecipeIngredientUse, Ingredient, RecipeStep
from app.recipe.recipe_forms import RecipeForm

from app.recipe import recipe_blueprint as bp_recipe

# for file upload
from werkzeug.utils import secure_filename
import uuid
import os


# checks that the ingredient form is valid, used before saving an ingredient use
def validRecipeIngredientUseForm(ingredientRel):
    if ingredientRel.ingredientName.data == "":
        # blank name, invalid
        return False
    elif ingredientRel.quantity.data <= 0:
        # negative or 0 quantity, invalid
        return False
    else:
        return True


# saves the data in the recipe form
def saveRecipeDraft(recipe_id, rform, picture=None):
    # get recipe object from the db
    recipeDraft = db.session.get(Recipe, recipe_id)

    # change and commit basic recipe data from the form
    recipeDraft.title = rform.title.data
    recipeDraft.description = rform.description.data
    recipeDraft.servingSize = rform.servingSize.data
    recipeDraft.estimatedHrs = rform.estimatedHrs.data
    recipeDraft.estimatedMins = rform.estimatedMins.data
    # recipeDraft.steps = rform.steps.data
    for s in recipeDraft.get_steps():
        db.session.delete(s)
        db.session.commit()#recipeDraft.recipe_steps.remove(s)
    i = 1
    for s in rform.steps:
        if s.stepDescription.data != "":
            recipeStep = RecipeStep(
                stepNum = i,
                description = s.stepDescription.data,
                recipe_id = recipe_id,
            )
            print("--")
            print(i)
            print(s.stepDescription.data)
            recipeDraft.recipe_steps.add(recipeStep)
            i += 1

    for t in recipeDraft.get_tags():
        recipeDraft.tags.remove(t)
    for t in rform.tags.data:
        recipeDraft.tags.add(t)
    recipeDraft.timestamp = datetime.now(timezone.utc)
    db.session.commit()

    # go through the ingredient fields in the form to check if the ingredients have been changed or added
    for ingredientRel in rform.ingredients:
        ingredientName = ingredientRel.ingredientName.data.lower()
        # if statement to ignore blank ingredients
        if validRecipeIngredientUseForm(ingredientRel):
            # check if an ingredient with this name exists in the db
            ingredientItem = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == ingredientName)).first()
            if ingredientItem is None:
                # ingredient doesn't exist, so add it
                # create and commit ingredient object to db
                ingredientItem = Ingredient(name=ingredientName)
                db.session.add(ingredientItem)
                db.session.commit()
                # create and commit the ingredient use case to the db
                newIngredientUse = RecipeIngredientUse(
                    recipe_id = recipe_id,
                    ingredient_id = ingredientItem.id,
                    amount = ingredientRel.quantity.data,
                    unit = ingredientRel.unit.data
                )
                db.session.add(newIngredientUse)
                db.session.commit()
            else:
                # ingredient exists, check if it already has an ingredient use for this recipe in db
                ingredientUse = db.session.get(RecipeIngredientUse, (recipe_id, ingredientItem.id))
                if ingredientUse is None:
                    # isn't in db yet, so add it
                    # create and commit the ingredient use case to the db
                    newIngredientUse = RecipeIngredientUse(
                        recipe_id = recipe_id,
                        ingredient_id = ingredientItem.id,
                        amount = ingredientRel.quantity.data,
                        unit = ingredientRel.unit.data
                    )
                    db.session.add(newIngredientUse)
                    db.session.commit()
                else:
                    # ingredient use case already in db, so just update and commit values
                    ingredientUse.amount = ingredientRel.quantity.data
                    ingredientUse.unit = ingredientRel.unit.data
                    db.session.commit()

    # save uploaded image
    basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static/img/recipe-imgs')
    # save uploaded image filename
    if picture is not None and picture.filename != "":
        pictName = str(uuid.uuid1()) + "_" + secure_filename(picture.filename)
        img_path = os.path.join(basedir, pictName)
        recipeDraft.pictFile = pictName
        picture.save(img_path)
    db.session.commit()

# check if the recipe draft is publishable
def validateRecipeDraftForPost(recipe_id):
    recipeDraft = db.session.get(Recipe, recipe_id)
    errors = []

    # check title is not blank
    if recipeDraft.title == "":
        errors.append("Please add a title")
    
    # check description is not blank
    if recipeDraft.description == "":
        errors.append("Please add a description")

    # check serving size is not empty
    if recipeDraft.servingSize <= 0:
        errors.append("Please put in a serving size")

    # check estimated time is not blank
    if recipeDraft.estimatedHrs == 0 and recipeDraft.estimatedMins == 0:
        errors.append("Please add an estimated time")
    if recipeDraft.estimatedHrs < 0:
        errors.append("Please add a valid time")
    if recipeDraft.estimatedMins < 0:
        errors.append("Please add a valid time")

    # check steps is not blank
    if len(recipeDraft.get_steps()) == 0:
        errors.append("Please add steps")

    # check that there are ingredients
    if db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == recipe_id)).first() is None:
        errors.append("No ingredients found")
    return errors

# removes an ingredient use from a recipe (NOTE: does not remove the ingredient from the db)
def removeIngredient(recipe_id, ingredient_id):
    # get the ingredient use case
    ingredientToRemove = db.session.get(RecipeIngredientUse, (recipe_id, ingredient_id))
    if ingredientToRemove is None:
        flash("Error! Could not find ingredient in recipe")
    else:
        # Delete ingredient use case from db
        db.session.delete(ingredientToRemove)
        db.session.commit()
        flash("Successfully removed ingredient")

def deleteRecipe(recipe_id):
    therecipe = db.session.get(Recipe, recipe_id)
    if therecipe is not None:
        for t in therecipe.get_tags():
            therecipe.tags.remove(t)
        for recipeIngredient in db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == recipe_id)).all():
            db.session.delete(recipeIngredient)
        for step in db.session.scalars(sqla.select(RecipeStep).where(RecipeStep.recipe_id == recipe_id)).all():
            therecipe.recipe_steps.remove(step)
            db.session.delete(step)
        db.session.execute(sqla.delete(RecipeStep).where(RecipeStep.recipe_id == recipe_id))
        db.session.delete(therecipe)
        db.session.commit()
        return True
    return False
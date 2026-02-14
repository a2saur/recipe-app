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
            base_query = sqla.select(Recipe).where(Recipe.is_draft == False)
            if sort_form.sortby.data == "Title":
                recipes = base_query.order_by(Recipe.title)
            else:
                recipes = base_query.order_by(Recipe.timestamp.desc())
    if request.method == 'GET':
        recipes = sqla.select(Recipe).where(Recipe.is_draft == False).order_by(Recipe.timestamp.desc())
    all_recipes  = db.session.scalars(recipes).all() 
    return render_template('index.html', title="", recipes=all_recipes, form=empty_form, sortform = sort_form)

@bp_main.route('/recipe/<recipe_id>/view', methods=['GET'])
# @login_required
def viewRecipe(recipe_id):
    theRecipe = db.session.scalars(sqla.select(Recipe).where(Recipe.id == recipe_id)).first()
    if not (theRecipe is None):
        theIngredients = db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == recipe_id)).all()
        return render_template('view_recipe.html', recipe = theRecipe, ingredients = theIngredients)
    return redirect(url_for('main.index'))


@bp_main.route('/recipe/create', methods=['GET', 'POST'])
# @login_required
# createRecipe shows the current recipe drafts and the option to create a new one
# the user will select one of these options and the system will redirect correspondingly
def createRecipe():
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
                return redirect(url_for('main.editRecipe', recipe_id=recipeDraft.id))
            else:
                # old recipe
                return redirect(url_for('main.editRecipe', recipe_id=int(buttonVal)))
        else:
            # delete recipe
            return url_for('main.delete', recipe_id=int(buttonVal))


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
def saveRecipeDraft(recipe_id, rform):
    # get recipe object from the db
    recipeDraft = db.session.get(Recipe, recipe_id)

    # change and commit basic recipe data from the form
    recipeDraft.title = rform.title.data
    recipeDraft.description = rform.description.data
    recipeDraft.servingSize = rform.servingSize.data
    recipeDraft.estimatedTime = rform.estimatedTime.data
    recipeDraft.steps = rform.steps.data
    for t in recipeDraft.get_tags():
        recipeDraft.tags.remove(t)
    for t in rform.tags.data :
            recipeDraft.tags.add(t)
    recipeDraft.timestamp = datetime.now(timezone.utc)
    db.session.commit()

    # go through the ingredient fields in the form to check if the ingredients have been changed or added
    for ingredientRel in rform.ingredients:
        # if statement to ignore blank ingredients
        if validRecipeIngredientUseForm(ingredientRel):
            # check if an ingredient with this name exists in the db
            ingredientItem = db.session.scalars(sqla.select(Ingredient).where(Ingredient.name == ingredientRel.ingredientName.data)).first()
            if ingredientItem is None:
                # ingredient doesn't exist, so add it
                # create and commit ingredient object to db
                ingredientItem = Ingredient(name=ingredientRel.ingredientName.data)
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
    if recipeDraft.estimatedTime == "":
        errors.append("Please add an estimated time")

    # check steps is not blank
    if recipeDraft.steps == "":
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

@bp_main.route('/recipe/<recipe_id>/edit', methods=['GET', 'POST'])
# @login_required
def editRecipe(recipe_id):
    # get the associated recipe draft
    recipeDraft = db.session.get(Recipe, recipe_id)

    if request.method == "GET":
        # pre-fill the recipe draft data
        # populate ingredient forms
        ingredient_data = []
        for ingUseCase in db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == recipe_id)).all():
            ingredient_data.append({
                "ingredientName": ingUseCase.recipe_usecase_ingredient.name,
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
            # save changes
            saveRecipeDraft(recipe_id=recipe_id, rform=rform)
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
            # add ingredient

            # save changes
            saveRecipeDraft(recipe_id=recipe_id, rform=rform)

            # redirect back to the edit recipe page
            return redirect(url_for('main.editRecipe', recipe_id=recipe_id))
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
            return redirect(url_for('main.editRecipe', recipe_id=recipe_id))
    if recipeDraft.is_draft:
        return render_template('create_recipe.html', title="Create New Recipe", form=rform, recipe_id=recipe_id, is_draft=True)
    else:
        return render_template('create_recipe.html', title="Edit Recipe", form=rform, recipe_id=recipe_id, is_draft=False)


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
def delete(recipe_id, redirectURL='main.index'):
    therecipe = db.session.scalars(sqla.select(Recipe).where(Recipe.id == recipe_id)).first()
    if therecipe is not None:
        for t in therecipe.get_tags():
            therecipe.tags.remove(t)
        db.session.commit()
        db.session.delete(therecipe)
        db.session.commit()
        flash('The recipe {} has been successfully deleted'.format(therecipe.title))
        return redirect(url_for(redirectURL))
    
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

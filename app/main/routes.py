import sys
from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from flask_login import current_user, login_required

from app import db
from app.main.models import Recipe, Tag, User, recipe_tags_table
from app.main.forms import RecipeForm, EmptyForm, SortForm, EditForm
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


@bp_main.route('/recipe/create', methods=['GET', 'POST'])
# @login_required
def postRecipe():
    pform = RecipeForm()
    if pform.validate_on_submit():
        recipe = Recipe(
            title = pform.title.data,
            body = pform.body.data,
            user_id = current_user.id
        )
        db.session.add(recipe)
        db.session.flush()
        for t in pform.tag.data:
            recipe.tags.add(t)
        db.session.commit()
        flash(f'Your recipe "{recipe.title}" is created!')
        return redirect(url_for('main.index'))
    return render_template('create.html', title="", form=pform)

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

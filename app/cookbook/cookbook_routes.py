from datetime import datetime, timezone
import sys

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
import sqlalchemy as sqla
from app import db

# for file upload
from werkzeug.utils import secure_filename
import uuid
import os

from app.main.models import Cookbook
from app.cookbook.cookbook_forms import CookbookForm

from app.cookbook import cookbook_blueprint as bp_cookbook

@bp_cookbook.route('/cookbook/create', methods=['GET', 'POST'])
@login_required
def create_cookbook():
    cform = CookbookForm()
    cform.recipes.query_factory = current_user.get_user_recipes
    if cform.validate_on_submit():
        cb = Cookbook(
            title=cform.title.data,
            description=cform.description.data,
            user_id=current_user.id
        )
        
        for r in cform.recipes.data :
            cb.included_recipes.add(r)
        
        db.session.commit()

        # save uploaded image
        basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static/img/recipe-imgs')
        # save uploaded image filename
        picture = request.files['pictFile']
        if picture is not None and picture.filename != "":
            pictName = str(uuid.uuid1()) + "_" + secure_filename(picture.filename)
            img_path = os.path.join(basedir, pictName)
            cb.pictFile = pictName
            picture.save(img_path)

        db.session.add(cb)
        db.session.commit()
        flash('Cookbook {} has been created'.format(cb.title))
        return redirect(url_for('main.index'))
    return render_template('create_cookbook.html', title='Create Cookbook', form=cform, editing_cookbook=False)

@bp_cookbook.route('/cookbook/<cookbook_id>/view', methods=['GET', 'POST'])
# @login_required
def view_cookbook():
    return redirect(url_for('main.index'))

@bp_cookbook.route('/cookbook/<cookbook_id>/edit', methods=['GET', 'POST'])
# @login_required
def edit_cookbook(cookbook_id):
    cookbookObj = db.session.get(Cookbook, cookbook_id)
    if cookbookObj is None:
        flash('Could not find cookbook')
        return redirect(url_for('main.index'))
    
    if request.method == "GET":
        cform = CookbookForm(
            title = cookbookObj.title,
            description = cookbookObj.description,
        )
        cform.recipes.query_factory = current_user.get_user_recipes
        cform.recipes.data = cookbookObj.get_recipes()
    else:
        cform = CookbookForm()
        cform.recipes.query_factory = current_user.get_user_recipes

    if cform.validate_on_submit():
        cookbookObj.title = cform.title.data
        cookbookObj.description = cform.description.data
        
        # remove old recipes
        for r in cookbookObj.get_recipes():
            cookbookObj.included_recipes.remove(r)

        for r in cform.recipes.data:
            cookbookObj.included_recipes.add(r)
        
        db.session.commit()

        # save uploaded image
        basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static/img/recipe-imgs')
        # save uploaded image filename
        picture = request.files['pictFile']
        if picture is not None and picture.filename != "":
            pictName = str(uuid.uuid1()) + "_" + secure_filename(picture.filename)
            img_path = os.path.join(basedir, pictName)
            cookbookObj.pictFile = pictName
            picture.save(img_path)

        db.session.commit()
        flash('Cookbook {} has been modified'.format(cookbookObj.title))
        return redirect(url_for('main.index'))
    return render_template('create_cookbook.html', title='Create Cookbook', form=cform, editing_cookbook=True, pictFile=cookbookObj.pictFile, cookbook_id=cookbookObj.id)


@bp_cookbook.route('/cookbook/<cookbook_id>/delete', methods=['POST'])
# @login_required
def delete_cookbook(cookbook_id):
    cookbookObj = db.session.get(Cookbook, cookbook_id)
    if cookbookObj is None:
        flash('Could not find cookbook')
        return redirect(url_for('main.index'))
    db.session.delete(cookbookObj)
    db.session.commit()
    flash("Cookbook successfully deleted")
    return redirect(url_for('main.index'))
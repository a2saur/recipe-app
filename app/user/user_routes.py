from datetime import datetime, timezone
import sys

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
import sqlalchemy as sqla
from app import db

from app.user.user_forms import EditForm

from app.user import user_blueprint as bp_user


@bp_user.route('/user/profile', methods=['GET','POST'])
# @login_required
def display_profile():
    return render_template('profile.html', title="User Profile", user=current_user)

@bp_user.route('/user/profile/edit', methods=['GET','POST'])
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
        return redirect(url_for('user.display_profile'))
    elif request.method == 'GET':
        eform.username.data = current_user.username
        eform.first_name.data = current_user.first_name
        eform.last_name.data = current_user.last_name
        eform.email.data = current_user.email
    return render_template('edit_profile.html', title="Edit Profile", form=eform, user=current_user)

@bp_user.route('/user/<recipe_id>/saverecipe', methods=['POST'])
# @login_required
def save_recipe(recipe_id):
    return

@bp_user.route('/user/<recipe_id>/removerecipe', methods=['POST'])
# @login_required
def remove_saved_recipe(recipe_id):
    return

@bp_user.route('/user/ingredients', methods=['GET','POST'])
# @login_required
def view_ingredients():
    return render_template('profile.html', title="User Profile", user=current_user)

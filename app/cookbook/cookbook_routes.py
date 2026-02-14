from datetime import datetime, timezone
import sys

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
import sqlalchemy as sqla
from app import db

from app.main.models import Recipe
from app.cookbook.cookbook_forms import *

from app.cookbook import cookbook_blueprint as bp_cookbook

@bp_cookbook.route('/cookbook/create', methods=['GET', 'POST'])
# @login_required
def create_cookbook():
    return redirect(url_for('main.index'))

@bp_cookbook.route('/cookbook/<cookbook_id>/view', methods=['GET', 'POST'])
# @login_required
def view_cookbook():
    return redirect(url_for('main.index'))

@bp_cookbook.route('/cookbook/<cookbook_id>/edit', methods=['GET', 'POST'])
# @login_required
def edit_cookbook():
    return redirect(url_for('main.index'))

@bp_cookbook.route('/cookbook/<cookbook_id>/delete', methods=['POST'])
# @login_required
def delete_cookbook():
    return
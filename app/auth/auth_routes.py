from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db, oauth
import os
from app.auth import auth_blueprint as bp_auth 
import sqlalchemy as sqla
from sqlalchemy import func
from app.auth.auth_forms import RegistrationForm, LoginForm
from app.main.models import Tag, User, Ingredient, user_allergies, user_preferred_tags, user_dietary_tags
from functools import wraps

@bp_auth.route('/login/callback')
def google_authorize():
    # 1. Get the data from Google
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if not user_info:
        flash("Failed to retrieve user info.")
        return redirect(url_for('auth.login'))

    email = user_info['email']
    # 2. Check if user exists (case-insensitive search to match your login logic)
    user = db.session.scalars(
        sqla.select(User).where(func.lower(User.email) == email.lower())
    ).first()

    # 3. Create user if they don't exist
    if not user:
        # We generate a random username if one isn't provided by Google
        # or use their name from Google
        new_username = user_info.get('preferred_username') or email.split('@')[0]
        
        user = User(
            first_name=user_info.get('given_name', 'SSO'),
            last_name=user_info.get('family_name', 'User'),
            username=new_username,
            email=email,
            is_certified=False
        )
        # Set a random password because User model likely requires one
        user.set_password(os.urandom(24).hex()) 
        db.session.add(user)
        db.session.commit()

    # 4. Log the user in
    login_user(user)
    flash('Welcome back, {}!'.format(user.first_name))
    return redirect(url_for('main.index'))

@bp_auth.route('/login/google')
def google_login():
    # Redirects to Google's auth page
    redirect_uri = url_for('auth.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


def clear_certify_email(func):
    @wraps(func)
    def wrapper(*args, ** kwargs):
        session.pop('from_reg', None)
        session.pop('reg_email', None)
        return func(*args, **kwargs)
    return wrapper

@bp_auth.route('/user/register', methods=['GET', 'POST'])
@clear_certify_email
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    rform = RegistrationForm()

    if rform.validate_on_submit():
        
        user = User(
            first_name = rform.first_name.data,
            last_name = rform.last_name.data,
            username = rform.username.data,
            email = rform.email.data,
            is_certified = False,
        )
        user.set_password(rform.password.data)
        db.session.add(user)
        db.session.flush() # flush to get the user id

        # add allergies
        if rform.allergies.data:
            for allergy in rform.allergies.data:
                ing_name = allergy.get('ingredientName').lower()
            
                ingredient = db.session.scalar(sqla.select(Ingredient).where(Ingredient.name == ing_name))

                if not ingredient:
                    ingredient = Ingredient(name=ing_name)
                    db.session.add(ingredient)
                    db.session.flush() # flush to get the ingredient id

                allergy = db.session.get(Ingredient, ingredient.id)
                user.allergies.add(allergy)

        # add all the preferred tags
        if rform.tags.data:
            for tag in rform.tags.data:
                tag = db.session.get(Tag, tag.id)
                user.preferred_tags.add(tag)
                

        # add all the dietary restriction tags
        if rform.dietary_restrictions.data:
            for tag in rform.dietary_restrictions.data:
                tag = db.session.get(Tag, tag.id)
                user.dietary_tags.add(tag)

        db.session.commit()
        flash('User {} {} has been registered.'.format(user.first_name, user.last_name))
        if rform.user_type.data == 'certified':
            session['from_reg'] = True
            session['reg_email'] = user.email
            return redirect(url_for('user.become_certified'))
        return redirect(url_for('auth.login'))
      
    # Check if the list is empty and add an entry if it is
    if request.method == 'GET' and not rform.allergies:
        rform.allergies.append_entry()

    return render_template('register.html', title='Register', form=rform)

@bp_auth.route('/user/login', methods=['GET', 'POST'])
@clear_certify_email
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    lform = LoginForm()
    if lform.validate_on_submit():
        user = db.session.scalars(sqla.select(User).where(func.lower(User.username) == lform.username.data.lower())).first()
        if user is None or not user.check_password(lform.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=lform.remember_me.data)
        flash('Welcome back, {}!'.format(user.first_name))
        return redirect(url_for('main.index'))
    return render_template('login.html', form=lform)


@bp_auth.route('/user/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
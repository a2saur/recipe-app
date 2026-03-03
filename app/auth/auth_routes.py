from flask import render_template, flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import auth_blueprint as bp_auth 
import sqlalchemy as sqla
from sqlalchemy import func
from app.auth.auth_forms import RegistrationForm, LoginForm
from app.main.models import User

@bp_auth.route('/user/register', methods=['GET', 'POST'])
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
        db.session.commit()
        flash('User {} {} has been registered.'.format(user.first_name, user.last_name))
        if rform.user_type.data == 'certified':
            session['from_reg'] = True
            session['reg_email'] = user.email
            return redirect(url_for('user.become_certified'))
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=rform)

@bp_auth.route('/user/login', methods=['GET', 'POST'])
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
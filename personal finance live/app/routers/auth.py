# app/routers/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms.forms import LoginForm, RegistrationForm

bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_blueprint = bp
# -------------------------------------------------
# LOGIN
# -------------------------------------------------
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next') or url_for('main.index')
            flash('Welcome back!', 'success')
            return redirect(next_page)
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

# -------------------------------------------------
# REGISTER
# -------------------------------------------------
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data, method='sha256')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! You can now log in.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'danger')
        else:
            print("Form errors:", form.errors)       # 5. validation failed?
        
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

# -------------------------------------------------
# LOGOUT
# -------------------------------------------------
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.index'))
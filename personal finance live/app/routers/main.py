# app/routers/main.py
from flask import Blueprint, redirect, url_for
from flask_login import current_user

bp = Blueprint('main', __name__)
main_blueprint = bp




@main_blueprint.route('/')
def index():
    """Root URL: if user is anonymous → login page, else → dashboard."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))
    
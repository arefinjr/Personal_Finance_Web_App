# app/routers/investments.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms.forms import InvestmentForm
from app.models import Investment
from flask_login import current_user, login_required
from app import db
import requests

bp = Blueprint('investments', __name__, url_prefix='/investments')
investment_blueprint = bp

# Function to fetch real-time market data
def fetch_real_time_data():
    api_key = 'YOUR_API_KEY'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={api_key}'
    response = requests.get(url)
    return response.json()

@investment_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = InvestmentForm()
    if form.validate_on_submit():
        new_investment = Investment(
            user_id=current_user.id,
            investment_type=form.investment_type.data,
            amount=form.amount.data,
            currency=form.currency.data,
            is_eco_friendly=form.is_eco_friendly.data
        )
        db.session.add(new_investment)
        db.session.commit()
        flash('Investment added!', 'success')
        return redirect(url_for('investments.index'))

    user_investments = Investment.query.filter_by(user_id=current_user.id).all()
    market_data = fetch_real_time_data()
    return render_template('investment.html', form=form, investments=user_investments, market_data=market_data)

@investment_blueprint.route('/<int:investment_id>/delete', methods=['POST'])
@login_required
def delete_investment(investment_id):
    investment = Investment.query.get_or_404(investment_id)
    if investment.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('investments.index'))
    db.session.delete(investment)
    db.session.commit()
    flash('Investment deleted!', 'info')
    return redirect(url_for('investments.index'))

@investment_blueprint.route('/<int:investment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_investment(investment_id):
    investment = Investment.query.get_or_404(investment_id)
    if investment.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('investments.index'))

    form = InvestmentForm(obj=investment)
    if form.validate_on_submit():
        investment.investment_type = form.investment_type.data
        investment.amount = form.amount.data
        investment.currency = form.currency.data
        investment.is_eco_friendly = form.is_eco_friendly.data
        db.session.commit()
        flash('Investment updated!', 'success')
        return redirect(url_for('investments.index'))

    return render_template('edit_investment.html', form=form, investment=investment)
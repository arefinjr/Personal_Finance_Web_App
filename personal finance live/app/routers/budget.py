# app/routers/budget.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Budget
from app.forms.forms import BudgetForm

bp = Blueprint('budget', __name__, url_prefix='/budget')
budget_blueprint = bp

# -------------------------------------------------
# LIST  (GET /budget)
# -------------------------------------------------
@budget_blueprint.route('/', methods=['GET'])
@login_required
def budget():
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    form = BudgetForm()
    return render_template('budget.html', budgets=budgets, form=form)

# -------------------------------------------------
# ADD  (POST /budget/add)
# -------------------------------------------------
@budget_blueprint.route('/add', methods=['POST'])
@login_required
def add_budget():
    form = BudgetForm()
    if form.validate_on_submit():
        existing = Budget.query.filter_by(user_id=current_user.id,
                                  name =form.name.data).first()
        if existing:
            existing.amount = form.amount.data
            flash('Budget updated!', 'info')
        else:
            new_budget = Budget(user_id=current_user.id,
                name =form.name.data,
                amount=form.amount.data,
                end_date = form.end_date.data)
                
                
            db.session.add(new_budget)
            flash('Budget created!', 'success')
        db.session.commit()
    else:
        for _, errors in form.errors.items():
            for e in errors:
                flash(e, 'danger')
    return redirect(url_for('budget.budget'))

# -------------------------------------------------
# EDIT  (GET/POST /budget/<int:budget_id>/edit)
# -------------------------------------------------
@budget_blueprint.route('/<int:budget_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_budget(budget_id):
    budget_item = Budget.query.get_or_404(budget_id)
    if budget_item.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('budget.budget'))

    form = BudgetForm(obj=budget_item)
    if form.validate_on_submit():
        budget_item.category = form.category.data
        budget_item.amount = form.amount.data
        db.session.commit()
        flash('Budget updated!', 'info')
        return redirect(url_for('budget.budget'))

    return render_template('budget.html', form=form, budgets=[budget_item])

# -------------------------------------------------
# DELETE  (POST /budget/<int:budget_id>/delete)
# -------------------------------------------------
@budget_blueprint.route('/<int:budget_id>/delete', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget_item = Budget.query.get_or_404(budget_id)
    if budget_item.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('budget.budget'))

    db.session.delete(budget_item)
    db.session.commit()
    flash('Budget deleted!', 'info')
    return redirect(url_for('budget.budget'))
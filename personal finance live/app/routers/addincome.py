from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app import db
from app.models import Income
from app.forms.forms import IncomeForm

bp = Blueprint('addincome', __name__, url_prefix='/addincome')
income_blueprint = bp


@income_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def income():
    form = IncomeForm()
    if form.validate_on_submit():
        new_income = Income(
            user_id=current_user.id,
            amount_per_month=form.amount_per_month.data,
            income_source_name=form.Income_Source_Name.data,
            partnership=form.Partnership.data or '',
            type=form.type.data,
            date=form.date.data
        )
        db.session.add(new_income) 
        db.session.commit()
        flash('Income recorded!', 'success')
        return redirect(url_for('addincome.income'))

    income = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).all()
    return render_template('addincome.html', form=form, addincome=income)

# Edit Income
@income_blueprint.route('/<int:income_id>/edit', methods=['GET', 'POST'])
def edit_income(income_id):
    income = Income.query.get_or_404(income_id)
    if income.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('addincome.income'))

    form = IncomeForm(obj=income)
    if form.validate_on_submit():
        income.income_source_name = form.Income_Source_Name.data
        income.amount_per_month   = form.amount_per_month.data
        income.partnership        = form.Partnership.data or ''
        income.type               = form.type.data
        income.date               = form.date.data
        db.session.commit()
        flash('Income updated!', 'info')
        return redirect(url_for('addincome.income'))
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    return render_template('addincome.html', form=form, income=incomes)


@income_blueprint.route('/<int:income_id>/delete', methods=['POST'])
@login_required
def delete_income(income_id):
    income = Income.query.get_or_404(income_id)
    if income.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('addincome.income'))

    db.session.delete(income)
    db.session.commit()
    flash('Income deleted!', 'info')
    return redirect(url_for('addincome.income'))
@income_blueprint.route('/<int:income_id>/view', methods=['GET'])
@login_required
def view_income(income_id):
    inc = Income.query.get_or_404(income_id)          # ← fetch from DB
    if inc.user_id != current_user.id:                # security check
        abort(403)

    return render_template('view_income.html', income=inc)
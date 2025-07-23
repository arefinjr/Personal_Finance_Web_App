from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Liability
from app.forms.forms import LiabilityForm

bp = Blueprint('liability', __name__, url_prefix='/liability')
liability_blueprint = bp   # exported alias


@liability_blueprint.route('/liability', methods=['GET', 'POST'])
@login_required
def add_liability():
    form = LiabilityForm()
    if form.validate_on_submit():
        liab = Liability(
            user_id=current_user.id,
            name=form.name.data,
            type_=form.type.data,
            balance=form.principal_amount.data,
            interest_rate=form.interest_rate.data,
            monthly_payment=form.emi_amount.data,
            due_date=form.due_date.data,
            # extended fields
            principal_amount=form.principal_amount.data,
            period_months=form.period_months.data,
            start_date=form.start_date.data,
            emi_amount=form.emi_amount.data,
            is_floating=form.is_floating.data,
            has_penalty=form.has_penalty.data,
            penalty_rate=form.penalty_rate.data,
            notes=form.notes.data,
        )
        db.session.add(liab)
        db.session.commit()
        flash('Liability added successfully!', 'success')
        return redirect(url_for('liability.add_liability'))
    txs = Liability.query.filter_by(user_id=current_user.id).order_by(Liability.start_date.desc()).all()
    return render_template('liability.html', form=form, liabilities = txs )



@liability_blueprint.route('/<int:liability_id>/delete', methods=['POST'])
@login_required
def delete_liability(liability_id):
    liab = Liability.query.get_or_404(liability_id)
    if liab.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('liability.add_liability'))

    db.session.delete(liab)
    db.session.commit()
    flash('Liability deleted.', 'info')
    return redirect(url_for('liability.add_liability'))
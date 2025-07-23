# app/routers/transactions.py
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Transaction
from app.forms.forms import TransactionForm



bp = Blueprint('transactions', __name__, url_prefix='/transactions')
transactions_blueprint = bp


@transactions_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def transactions():
    form = TransactionForm()
    if form.validate_on_submit():
        tx = Transaction(
            user_id=current_user.id,
            description=form.description.data,
            amount=form.amount.data,
            category=form.category.data,
            type=form.tx_type.data,
            date=form.date.data
        )
        db.session.add(tx) 
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions.transactions'))

    # show user’s own transactions
    txs = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', form=form, transactions=txs)


# -------------------------------------------------
# DELETE  (POST /budget/<int:budget_id>/delete)
# -------------------------------------------------
@transactions_blueprint.route('/<int:transaction_id>/delete', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction_item = Transaction.query.get_or_404(transaction_id)
    if transaction_item.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('transactions.transactions'))

    db.session.delete(transaction_item)
    db.session.commit()
    flash('Transaction deleted!', 'info')
    return redirect(url_for('transactions.transactions'))
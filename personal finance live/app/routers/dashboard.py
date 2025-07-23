from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from flask import render_template, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import func
from app import db
from app.models import (
    Income, Budget, Transaction, Liability, Asset,
    NetWorthSnapshot, Envelope, Goal, ScheduledTransaction
)
from app.utils.finance_health import calculate_health_score
from collections import defaultdict

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
dashboard_blueprint = bp

def get_monthly_totals(user_id, year):
    """Returns income and expense totals per month for a given user and year."""
    monthly_income = defaultdict(float)
    monthly_expenses = defaultdict(float)

    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= f"{year}-01-01",
        Transaction.date <= f"{year}-12-31"
    ).all()

    for txn in transactions:
        month = txn.date.strftime('%b')  # 'Jan', 'Feb', etc.
        if txn.type == 'income':
            monthly_income[month] += txn.amount
        elif txn.type == 'expense':
            monthly_expenses[month] += txn.amount

    # Ensure all months are represented
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    income_list = [round(monthly_income[m], 2) for m in months]
    expense_list = [round(monthly_expenses[m], 2) for m in months]

    return income_list, expense_list

def _round(val: float, digits: int = 2) -> float:
    """Bankers rounding via Decimal."""
    return float(Decimal(str(val)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


@dashboard_blueprint.route('/')
@login_required
def dashboard():
    user_id = current_user.id
    today = datetime.utcnow().date()
    current_month = today.strftime('%Y-%m')

    # 1. Cash-flow
    total_income   = _round(sum(i.amount_per_month for i in Income.query.filter_by(user_id=user_id)))
    total_expenses = _round(sum(b.amount for b in Budget.query.filter_by(user_id=user_id)))
    savings        = _round(total_income - total_expenses)

    # 2. Balance-sheet
    assets       = db.session.query(func.coalesce(func.sum(Asset.value), 0)).filter_by(user_id=user_id).scalar() or 0
    liabilities = db.session.query(func.coalesce(func.sum(Liability.balance), 0)).filter_by(user_id=user_id).scalar() or 0
    net_worth_val = _round(assets - liabilities)

    # 2A. Net-worth snapshot
    if not NetWorthSnapshot.query.filter_by(user_id=user_id, date=today).first():
        db.session.add(NetWorthSnapshot(user_id=user_id, date=today, amount=net_worth_val))
        db.session.commit()

    # 3. Funds & ratios
    family_fund      = _round(total_income * 0.50)
    emergency_factor = (1 + 0.06/12) ** 6
    emergency_fund   = _round(total_expenses * 6 * emergency_factor)
    medical_fund     = _round(total_income * 0.05)
    security_fund    = _round(total_income * 0.03)
    maintenance_fund = _round(total_income * 0.10)
    loan_balance     = _round(liabilities)
    dti_ratio        = _round(float(liabilities) / max(total_income, 1) * 100, 1)

    allocated = (
        family_fund
        + emergency_fund / 12
        + medical_fund
        + security_fund
        + maintenance_fund
        + loan_balance / 12
    )
    free = _round(max(total_income - allocated, 0))

    health_score = calculate_health_score(total_income, total_expenses)
    fi_number    = _round(total_expenses * 12 * 25)

    # 4. Envelopes, Goals, Scheduled, Recent
    envelopes   = Envelope.query.filter_by(user_id=user_id, month=current_month).all()
    goals       = Goal.query.filter_by(user_id=user_id).all()
    upcoming    = ScheduledTransaction.query.filter(
        ScheduledTransaction.user_id == user_id,
        ScheduledTransaction.next_date <= today + timedelta(days=30)
    ).all()
    recent_transactions = (
        Transaction.query
        .filter_by(user_id=user_id)
        .order_by(Transaction.date.desc())
        .limit(5)
        .all()
    )

    # 5. Sparkline data (last 12 snapshots)
    sparkline = (
        db.session.query(NetWorthSnapshot.date, NetWorthSnapshot.amount)
        .filter_by(user_id=user_id)
        .order_by(NetWorthSnapshot.date.desc())
        .limit(12)
        .all()
    )
    sparkline_labels = [s.date.strftime('%b %d') for s in reversed(sparkline)]
    sparkline_data   = [float(s.amount)        for s in reversed(sparkline)]

    year = today.year
    monthly_income, monthly_expenses = get_monthly_totals(user_id, year)


    return render_template(
    'dashboard.html',
    income=total_income,
    expenses=total_expenses,
    savings=savings,
    networths=net_worth_val,
    family_fund=family_fund,
    emergency_fund=emergency_fund,
    medical=medical_fund,
    security=security_fund,
    maintenance_fund=maintenance_fund,
    loan=loan_balance,
    loan_dti=dti_ratio,
    free=free,
    health_score=health_score,
    fi_number=fi_number,
    recent_transactions=recent_transactions,
    envelopes=envelopes,
    goals=goals,
    upcoming=upcoming,
    sparkline_labels=sparkline_labels,
    sparkline_data=sparkline_data,
    income_monthly=monthly_income,
    expenses_monthly=monthly_expenses
)
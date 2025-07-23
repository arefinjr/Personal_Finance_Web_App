from datetime import datetime
from flask_login import UserMixin  # only for User table
from sqlalchemy import Numeric
from app import db 

# User Info
class User(UserMixin, db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(80), unique=True, nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    password    = db.Column(db.String(128), nullable=False)   # hashed
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    transactions = db.relationship('Transaction', back_populates='user', lazy='dynamic')

# Income Info
class Income(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount_per_month    = db.Column(db.Float, nullable=False)
    income_source_name  = db.Column(db.String(100), nullable=False)
    partnership         = db.Column(db.Text, nullable=True)
    type                = db.Column(db.String(20), nullable=False)  # e.g. 'salary', 'freelance'
    date                = db.Column(db.Date, nullable=False)

    user = db.relationship('User', backref=db.backref('incomes', lazy='dynamic')) 

# liability info
class Liability(db.Model):
    """
    All user liabilities: loans, credit cards, BNPL
    """
    __tablename__ = "liabilities"

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name        = db.Column(db.String(120), nullable=False)          # e.g. "Home Loan"
    balance     = db.Column(db.Numeric(precision=12, scale=2), default=0.00)
    interest_rate = db.Column(db.Numeric(precision=5,  scale=2), default=0.00)   # % p.a.
    monthly_payment = db.Column(db.Numeric(precision=12, scale=2), default=0.00)
    type_       = db.Column(db.String(40), default="other")          # mortgage, credit_card, etc.
    due_date    = db.Column(db.Date)                                 # next EMI date
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, onupdate=datetime.utcnow)
    principal_amount = db.Column(db.Numeric(12, 2), default=0.00)    # original loan amount
    period_months    = db.Column(db.Integer, default=0)              # total tenure
    start_date       = db.Column(db.Date)                            # loan start
    emi_amount       = db.Column(db.Numeric(12, 2), default=0.00)    # monthly EMI
    is_floating      = db.Column(db.Boolean, default=False)           # floating rate flag
    has_penalty      = db.Column(db.Boolean, default=False)           # pre-payment penalty flag
    penalty_rate     = db.Column(db.Numeric(5, 2), default=0.00)      # penalty %
    notes            = db.Column(db.Text)                             # free-form notes
    debt_service_ratio = db.Column(db.Numeric(5, 2), default=0.00)

    # Relationships
    user = db.relationship("User", backref="liabilities")

#Asset info
class Asset(db.Model):
    """
    All user assets: cash, equities, real estate, gold, crypto, etc.
    """
    __tablename__ = "assets"

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name        = db.Column(db.String(120), nullable=False)          # e.g. "HDFC Liquid Fund"
    value       = db.Column(db.Numeric(precision=14, scale=2), default=0.00)
    type_       = db.Column(db.String(40), default="cash")           # cash, equity, real_estate, etc.
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship("User", backref="assets")



#transaction Info at database
class Transaction(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount      = db.Column(db.Float, nullable=False)          # positive for income, negative for expense
    type        = db.Column(db.String(8), nullable=False)      # 'income' | 'expense'
    category    = db.Column(db.String(50), default='Misc')
    date        = db.Column(db.Date, default=datetime.utcnow)

    # back-link
    user = db.relationship('User', back_populates='transactions')

# Budget info at database
class Budget(db.Model):
    
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name        = db.Column(db.String(100), nullable=False)        # e.g. "Groceries", "Vacation"
    amount      = db.Column(db.Float, nullable=False)              # planned amount
    period      = db.Column(db.String(10), default='monthly')      # daily / weekly / monthly / yearly
    start_date  = db.Column(db.Date, default=datetime.utcnow)
    end_date    = db.Column(db.Date, default=datetime.utcnow, nullable=True)

    # relationships
    user = db.relationship('User', backref=db.backref('budgets', lazy='dynamic'))

    def spent(self):
        """Sum of *expense* transactions that belong to this budget category."""
        return (
            db.session.query(db.func.sum(Transaction.amount))
            .filter(Transaction.user_id == self.user_id,
                    Transaction.category == self.name,
                    Transaction.type == 'expense')
            .scalar() or 0.0
        )

    def remaining(self):
        return self.amount + self.spent()   # spent() is negative

# Goal Info 

class Goal(db.Model):
    description = db.Column(db.Text, nullable=True)  # or String(255)
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title       = db.Column(db.String(120), nullable=False)
    target      = db.Column(db.Float, nullable=False)           # amount to reach
    saved       = db.Column(db.Float, default=0.0)              # current balance
    deadline    = db.Column(db.Date, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    
    # relationships
    user = db.relationship('User', backref=db.backref('goals', lazy='dynamic'))

    def progress_percent(self):
        if self.target <= 0:
            return 0
        return min(100.0, (self.saved / self.target) * 100)

# Reminder info
class Reminder(db.Model):
    id                   = db.Column(db.Integer, primary_key=True)
    user_id              = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description          = db.Column(db.String(255), nullable=False)
    due_date             = db.Column(db.Date, nullable=False)
    created_at           = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='reminders')

# app/models.py
class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    investment_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    currency = db.Column(db.String(10), default='USD')
    is_eco_friendly = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Investment {self.investment_type} - {self.amount}>'


# --------------------------------------------------
# YNAB-style Envelope (zero-based) budgets
# --------------------------------------------------
class Envelope(db.Model):
    __tablename__ = 'envelopes'
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category  = db.Column(db.String(64), nullable=False)
    budgeted  = db.Column(Numeric(12,2), default=0)   # planned amount
    spent     = db.Column(Numeric(12,2), default=0)   # negative = overspent
    month     = db.Column(db.String(7), nullable=False)  # YYYY-MM

# --------------------------------------------------
# Mint-style Net-worth history snapshots
# --------------------------------------------------
class NetWorthSnapshot(db.Model):
    __tablename__ = 'net_worth_snapshots'
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date      = db.Column(db.Date, nullable=False)
    amount    = db.Column(Numeric(12,2), nullable=False)

# --------------------------------------------------
# Personal-Capital-style Goals
# --------------------------------------------------
class Goal(db.Model):
    __tablename__ = 'goals'
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name          = db.Column(db.String(120), nullable=False)
    target_amount = db.Column(Numeric(12,2), nullable=False)
    current_amount= db.Column(Numeric(12,2), default=0)
    deadline      = db.Column(db.Date)

# --------------------------------------------------
# Monarch-style Scheduled (recurring) transactions
# --------------------------------------------------
class ScheduledTransaction(db.Model):
    __tablename__ = 'scheduled_transactions'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name       = db.Column(db.String(120))
    amount     = db.Column(Numeric(12,2), nullable=False)
    next_date  = db.Column(db.Date, nullable=False)
    frequency  = db.Column(db.String(16), default='monthly')  # weekly / monthly / yearly
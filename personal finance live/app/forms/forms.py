from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, FloatField, IntegerField, SelectField, DecimalField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Optional, Length
from app.models import User
from flask import current_app   # <= add this import at top
from datetime import datetime

# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        with current_app.app_context():          # create context needed by SQLAlchemy
            user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        with current_app.app_context():
            user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
class TransactionForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    amount      = FloatField('Amount', validators=[DataRequired()])
    category    = StringField('Category', validators=[DataRequired()])
    submit      = SubmitField('Add Transaction') 
    tx_type     = StringField('Transaction Type', validators=[DataRequired()])      # 'income' | 'expense'
    date        = DateField('Date')
# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
class BudgetForm(FlaskForm):
    name        = StringField('Category', validators=[DataRequired()])
    amount      = FloatField('Amount', validators=[DataRequired()])
    end_date    = DateField('Date', validators=[DataRequired()])
    submit      = SubmitField('Set Budget')
# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
class GoalForm(FlaskForm):
    title       = StringField('Title',        validators=[DataRequired()])
    description = TextAreaField('Description')  # <- NEW
    target      = FloatField('Target Amount', validators=[DataRequired()])
    deadline    = DateField('Deadline (optional)')   # add if you use it
    submit      = SubmitField('Set Goal')
    
# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
class InvestmentForm(FlaskForm):
    investment_type = SelectField(
        'Type',
        choices=[
            ('stocks', 'Stocks'),
            ('bonds', 'Bonds'),
            ('crypto', 'Cryptocurrency'),
            ('reits', 'REITs'),
            ('commodities', 'Commodities')
        ],
        validators=[DataRequired()]
    )
    amount = DecimalField(
        'Amount (USD)',
        places=2,
        validators=[
            DataRequired(),
            NumberRange(min=0.01, message='Amount must be greater than 0')
        ]
    )
    currency = StringField('Currency', validators=[DataRequired()])  
    is_eco_friendly = BooleanField('Eco-Friendly Investment')
    submit = SubmitField('Add')
# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
class ReminderForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    submit = SubmitField('Add Reminder')

# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
class IncomeForm(FlaskForm):
    amount_per_month    = FloatField('Amount Per Month', validators=[DataRequired(), NumberRange(min=0.01)])
    Income_Source_Name  = StringField('Income Source Name', validators=[DataRequired()])
    Partnership         = TextAreaField('Description Of Partnership (If Any)')
    type                = SelectField('Type', choices=[
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('investment', 'Investment'),
        ('gift', 'Gift'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    date                = DateField('Date', validators=[DataRequired()], default=datetime.today)
    submit              = SubmitField('Add Income') 
    # Delete Transaction
# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------

class LiabilityForm(FlaskForm):
    # Basic identification
    name = StringField(
        'Liability Name',
        validators=[DataRequired()],
        description='e.g. "SBI Home Loan", "HDFC Credit Card"'
    )

    # Detailed type
    type = SelectField(
        'Type',
        choices=[
            ('credit_card',      'Credit Card'),
            ('personal',         'Personal Loan'),
            ('mortgage',         'Home Loan / Mortgage'),
            ('auto',             'Car / Auto Loan'),
            ('education',        'Education Loan'),
            ('business',         'Business Loan'),
            ('bnpl',             'Buy-Now-Pay-Later'),
            ('maintenance',      'Maintenance / Subscription'),
            ('other',            'Other')
        ],
        validators=[DataRequired()]
    )

    # Monetary details
    principal_amount = FloatField(
        'Principal / Outstanding Balance (₹)',
        validators=[DataRequired(), NumberRange(min=0.01)]
    )

    interest_rate = FloatField(
        'Annual Interest Rate (%)',
        validators=[DataRequired(), NumberRange(min=0.0, max=100.0)]
    )

    period_months = IntegerField(
        'Total Tenure (months)',
        validators=[DataRequired(), NumberRange(min=1)]
    )

    emi_amount = FloatField(
        'Monthly EMI (₹)',
        validators=[DataRequired(), NumberRange(min=0.01)]
    )

    # Timing
    start_date = DateField(
        'Start Date',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )
    due_date = DateField(
        'Next Due Date',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )

    # Additional fields for deeper analysis
    is_floating = BooleanField('Floating Interest Rate?', default=False)
    has_penalty = BooleanField('Pre-payment Penalty?', default=False)
    penalty_rate = FloatField(
        'Pre-payment Penalty (%)',
        validators=[Optional(), NumberRange(min=0.0, max=100.0)]
    )

    notes = TextAreaField('Additional Notes', validators=[Optional()])

    # Financial ratios helper (not saved to DB, but used in analysis)
    debt_service_ratio = FloatField(
        'Current Debt-Service-to-Income Ratio (%)',
        validators=[Optional(), NumberRange(min=0.0, max=100.0)]
    )

# ------------- Envelope Form --------------
class EnvelopeForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired(), Length(max=64)])
    budgeted = DecimalField('Budgeted', validators=[DataRequired()], places=2)
    month    = StringField('Month (YYYY-MM)', validators=[DataRequired(), Length(7)])
    submit   = SubmitField('Save Envelope')

# ------------- Goal Form ------------------
class GoalForm(FlaskForm):
    name           = StringField('Goal name', validators=[DataRequired(), Length(max=120)])
    target_amount  = DecimalField('Target', validators=[DataRequired()], places=2)
    current_amount = DecimalField('Current', default=0, places=2)
    deadline       = DateField('Deadline', format='%Y-%m-%d')
    submit         = SubmitField('Create Goal')

# ------------- Scheduled Txn Form ---------
class ScheduledTransactionForm(FlaskForm):
    name       = StringField('Description', validators=[DataRequired()])
    amount     = DecimalField('Amount', validators=[DataRequired()], places=2)
    next_date  = DateField('Next date', format='%Y-%m-%d')
    frequency  = SelectField('Frequency', choices=[('weekly','Weekly'),
                                                   ('monthly','Monthly'),
                                                   ('yearly','Yearly')])
    submit     = SubmitField('Schedule')
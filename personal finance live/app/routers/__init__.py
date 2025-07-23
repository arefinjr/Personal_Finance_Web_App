from flask import Blueprint

# Import all route handlers
from app.routers.main import main_blueprint
from app.routers.auth import auth_blueprint
from app.routers.dashboard import dashboard_blueprint
from app.routers.transactions import transactions_blueprint
from app.routers.budget import budget_blueprint
from app.routers.goals import goals_blueprint
from app.routers.investment import investment_blueprint
from app.routers.reminders import reminders_blueprint
from app.routers.addincome import income_blueprint
from app.routers.liability import liability_blueprint

# Initialize and register Blueprints
def init_app(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    app.register_blueprint(transactions_blueprint, url_prefix='/transactions')
    app.register_blueprint(budget_blueprint, url_prefix='/budget')
    app.register_blueprint(goals_blueprint, url_prefix='/goals')
    app.register_blueprint(investment_blueprint, url_prefix='/investment')
    app.register_blueprint(reminders_blueprint, url_prefix='/reminders') 
    app.register_blueprint(income_blueprint, url_prefix='/addincome')
    app.register_blueprint(liability_blueprint, url_prefix='/liability')
    
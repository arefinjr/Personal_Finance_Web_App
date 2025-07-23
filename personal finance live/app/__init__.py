from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config.base import BaseConfig

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=BaseConfig):
    # Initialize Flask app
    app = Flask(__name__)

    # Load configuration settings
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # User loader
    with app.app_context():
        from app.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    # Register blueprints
    from app.routers.main import main_blueprint
    app.register_blueprint(main_blueprint)

    from app.routers.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.routers.dashboard import dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

    from app.routers.transactions import transactions_blueprint
    app.register_blueprint(transactions_blueprint, url_prefix='/transactions')

    from app.routers.budget import budget_blueprint
    app.register_blueprint(budget_blueprint, url_prefix='/budget')

    from app.routers.goals import goals_blueprint
    app.register_blueprint(goals_blueprint, url_prefix='/goals')

    from app.routers.investment import investment_blueprint
    app.register_blueprint(investment_blueprint, url_prefix='/investment')

    from app.routers.reminders import reminders_blueprint
    app.register_blueprint(reminders_blueprint, url_prefix='/reminders')

    from app.routers.liability import liability_blueprint
    app.register_blueprint(liability_blueprint, url_prefix='/liability')

    from app.routers.addincome import income_blueprint
    app.register_blueprint(income_blueprint)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
"""
Application factory – creates and configures the Flask app.
"""
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions (created here, attached to app in create_app)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to continue.'
login_manager.login_message_category = 'info'


def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__)

    # Load config
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    from config.settings import config_by_name
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # User loader for Flask-Login
    from app.models.user import User
    from app.models.user_profile import UserProfile

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register error handlers
    _register_error_handlers(app)

    return app


def _register_error_handlers(app):
    """Register custom error pages."""
    from flask import render_template

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template('errors/500.html'), 500

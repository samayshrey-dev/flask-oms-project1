"""
Routes package – registers all blueprints with the app.
"""
from app.routes.auth import auth_bp
from app.routes.customer import customer_bp
from app.routes.supplier import supplier_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(supplier_bp)

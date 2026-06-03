"""
AuthService – handles user registration and authentication logic.
"""
import logging
from app import db
from app.models.user import User
from app.models.cart import Cart

logger = logging.getLogger(__name__)


class AuthService:

    @staticmethod
    def register_user(name, email, password, role='customer'):
        """
        Register a new user. Creates a cart for customers automatically.
        Returns (user, error_message).
        """
        # Validate inputs
        if not all([name, email, password]):
            return None, 'All fields are required.'

        if role not in ('customer', 'supplier'):
            return None, 'Invalid role.'

        if len(password) < 6:
            return None, 'Password must be at least 6 characters.'

        # Check for existing email
        existing = User.query.filter_by(email=email.lower().strip()).first()
        if existing:
            return None, 'An account with this email already exists.'

        try:
            user = User(
                name=name.strip(),
                email=email.lower().strip(),
                role=role
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # Get user.id before commit

            # Auto-create cart for customers
            if role == 'customer':
                cart = Cart(user_id=user.id)
                db.session.add(cart)

            db.session.commit()
            logger.info(f'User registered: {user.email} as {user.role}')
            return user, None

        except Exception as e:
            db.session.rollback()
            logger.error(f'Registration failed: {e}')
            return None, 'Registration failed. Please try again.'

    @staticmethod
    def authenticate(email, password):
        """
        Verify credentials. Returns (user, error_message).
        """
        if not email or not password:
            return None, 'Email and password are required.'

        user = User.query.filter_by(email=email.lower().strip()).first()
        if not user or not user.check_password(password):
            return None, 'Invalid email or password.'

        logger.info(f'User authenticated: {user.email}')
        return user, None

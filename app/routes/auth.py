"""
Authentication routes – register, login, logout.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Redirect to appropriate dashboard or render landing page."""
    if current_user.is_authenticated:
        if current_user.is_supplier:
            return redirect(url_for('supplier.dashboard'))
        return redirect(url_for('customer.home'))
    return render_template('landing.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        role = request.form.get('role', 'customer')

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')

        user, error = AuthService.register_user(name, email, password, role)
        if error:
            flash(error, 'error')
            return render_template('auth/register.html')

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        user, error = AuthService.authenticate(email, password)
        if error:
            flash(error, 'error')
            return render_template('auth/login.html')

        login_user(user)
        flash(f'Welcome back, {user.name}!', 'success')
        
        # Role-based redirection
        if user.role == 'customer':
            return redirect(url_for('customer.home'))
        elif user.role == 'supplier':
            return redirect(url_for('supplier.dashboard'))
            
        return redirect(url_for('auth.index'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

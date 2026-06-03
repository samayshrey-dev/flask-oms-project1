"""
Customer routes – product browsing, cart, orders, payments.
All routes require login + 'customer' role.
"""
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models.product import Product
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')


def customer_required(f):
    """Decorator: ensures the logged-in user is a customer."""
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_customer:
            flash('Access denied. Customer account required.', 'error')
            abort(403)
        return f(*args, **kwargs)
    return decorated


@customer_bp.context_processor
def inject_customer_context():
    """Make categories globally available to all customer blueprint templates."""
    # We only need to fetch categories if the user is a customer, 
    # but the context processor runs for all templates rendered by this BP anyway.
    return dict(categories=ProductService.get_categories())


# ── Customer Home ────────────────────────────────────────────────
@customer_bp.route('/home')
@customer_required
def home():
    from sqlalchemy.sql.expression import func
    # Random mix of products from all categories
    products = Product.query.filter_by(is_active=True).order_by(func.rand()).limit(20).all()
    # Fetch existing categories dynamically
    categories = ProductService.get_categories()
    return render_template('customer/home.html', products=products, categories=categories)


# ── Customer Account ─────────────────────────────────────────────
@customer_bp.route('/account', methods=['GET', 'POST'])
@customer_required
def account():
    from app.models.user_profile import UserProfile
    from app import db
    
    # Ensure profile exists
    if not current_user.profile:
        new_profile = UserProfile(user_id=current_user.id)
        db.session.add(new_profile)
        db.session.commit()

    if request.method == 'POST':
        # Update user basics
        current_user.name = request.form.get('name', current_user.name)
        
        # Update profile
        profile = current_user.profile
        profile.phone = request.form.get('phone', profile.phone)
        profile.address_line1 = request.form.get('address_line1', profile.address_line1)
        profile.address_line2 = request.form.get('address_line2', profile.address_line2)
        profile.city = request.form.get('city', profile.city)
        profile.state = request.form.get('state', profile.state)
        profile.zip_code = request.form.get('zip_code', profile.zip_code)
        profile.country = request.form.get('country', profile.country)
        
        try:
            db.session.commit()
            flash('Your account details have been successfully updated.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating account details.', 'error')
            
        return redirect(url_for('customer.account'))

    from app.models.order import Order
    total_spent = db.session.query(db.func.sum(Order.total_amount)).filter_by(
        customer_id=current_user.id, status='delivered'
    ).scalar() or 0.0

    return render_template('customer/account.html', profile=current_user.profile, total_spent=total_spent)

# ── Product Browsing ─────────────────────────────────────────────
@customer_bp.route('/products')
@customer_required
def products():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    items = ProductService.get_active_products(search=search, category=category)
    categories = ProductService.get_categories()
    return render_template('customer/products.html',
                           products=items, categories=categories,
                           search=search, selected_category=category)


@customer_bp.route('/products/<int:product_id>')
@customer_required
def product_detail(product_id):
    product = ProductService.get_product_by_id(product_id)
    if not product or not product.is_active:
        flash('Product not found.', 'error')
        return redirect(url_for('customer.products'))
    return render_template('customer/product_detail.html', product=product)


# ── Cart ─────────────────────────────────────────────────────────
@customer_bp.route('/cart')
@customer_required
def cart():
    cart_data = CartService.get_cart_details(current_user.id)
    return render_template('customer/cart.html', cart=cart_data)


@customer_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@customer_required
def add_to_cart(product_id):
    qty = int(request.form.get('quantity', 1))
    next_page = request.args.get('next')
    ok, error = CartService.add_item(current_user.id, product_id, qty)
    if not ok:
        flash(error, 'error')
    else:
        flash('Added to cart!', 'success')
    return redirect(next_page or request.referrer or url_for('customer.products'))


@customer_bp.route('/api/cart/add/<int:product_id>', methods=['POST'])
@customer_required
def api_add_to_cart(product_id):
    """AJAX endpoint – adds to cart without page reload."""
    from flask import jsonify
    data = request.get_json(silent=True) or {}
    qty = int(data.get('quantity', 1))
    ok, error = CartService.add_item(current_user.id, product_id, qty)
    if not ok:
        return jsonify({'success': False, 'error': error}), 400
    # Return updated cart count
    cart_count = current_user.cart.item_count if current_user.cart else 0
    return jsonify({'success': True, 'cart_count': cart_count})


@customer_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@customer_required
def update_cart(item_id):
    qty = int(request.form.get('quantity', 1))
    ok, error = CartService.update_quantity(current_user.id, item_id, qty)
    if not ok:
        flash(error, 'error')
    else:
        flash('Cart updated.', 'success')
    return redirect(url_for('customer.cart'))


@customer_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@customer_required
def remove_from_cart(item_id):
    ok, error = CartService.remove_item(current_user.id, item_id)
    if not ok:
        flash(error, 'error')
    else:
        flash('Item removed.', 'info')
    return redirect(url_for('customer.cart'))


# ── Checkout & Orders ────────────────────────────────────────────
@customer_bp.route('/checkout', methods=['GET', 'POST'])
@customer_required
def checkout():
    cart_data = CartService.get_cart_details(current_user.id)
    if not cart_data or not cart_data.items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('customer.cart'))

    if request.method == 'POST':
        address = request.form.get('shipping_address', '')
        order, error = OrderService.place_order(current_user.id, address)
        if error:
            flash(error, 'error')
            return render_template('customer/checkout.html', cart=cart_data)
        flash(f'Order #{order.id} placed successfully!', 'success')
        return redirect(url_for('customer.orders'))

    return render_template('customer/checkout.html', cart=cart_data)


@customer_bp.route('/orders')
@customer_required
def orders():
    status_filter = request.args.get('status')
    user_orders = OrderService.get_customer_orders(current_user.id, status=status_filter)
    return render_template('customer/orders.html', orders=user_orders, current_status=status_filter)


@customer_bp.route('/orders/<int:order_id>')
@customer_required
def order_detail(order_id):
    order = OrderService.get_order_detail(order_id, customer_id=current_user.id)
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('customer.orders'))
    payment = PaymentService.get_payment_for_order(order_id)
    return render_template('customer/order_detail.html',
                           order=order, payment=payment)


@customer_bp.route('/orders/cancel/<int:order_id>', methods=['POST'])
@customer_required
def cancel_order(order_id):
    order = OrderService.get_order_detail(order_id, customer_id=current_user.id)
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('customer.orders'))
    
    if order.status != 'pending':
        flash('Only pending orders can be cancelled.', 'error')
        return redirect(url_for('customer.order_detail', order_id=order_id))
        
    ok, error = OrderService.update_order_status(order_id, supplier_id=None, new_status='cancelled', is_customer=True)
    if not ok:
        flash(error, 'error')
    else:
        flash(f'Order #{order.id} has been cancelled.', 'info')
    return redirect(url_for('customer.order_detail', order_id=order_id))


# ── Payment ──────────────────────────────────────────────────────
@customer_bp.route('/payment/<int:order_id>', methods=['GET', 'POST'])
@customer_required
def payment(order_id):
    order = OrderService.get_order_detail(order_id, customer_id=current_user.id)
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('customer.orders'))

    if order.status != 'pending':
        flash('Payment already processed or order is not in pending state.', 'info')
        return redirect(url_for('customer.order_detail', order_id=order_id))

    if request.method == 'POST':
        method = request.form.get('payment_method', '')
        payment_obj, error = PaymentService.process_payment(
            order_id, current_user.id, method
        )
        if error:
            flash(error, 'error')
            return render_template('customer/payment.html', order=order)

        if payment_obj.status == 'success':
            flash(f'Payment successful! Transaction: {payment_obj.transaction_id}',
                  'success')
        else:
            flash('Payment failed. Please try again.', 'error')
        return redirect(url_for('customer.order_detail', order_id=order_id))

    return render_template('customer/payment.html', order=order)

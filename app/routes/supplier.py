"""
Supplier routes – product management and order fulfillment.
All routes require login + 'supplier' role.
"""
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.services.product_service import ProductService
from app.services.order_service import OrderService

supplier_bp = Blueprint('supplier', __name__, url_prefix='/supplier')


def supplier_required(f):
    """Decorator: ensures the logged-in user is a supplier."""
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_supplier:
            flash('Access denied. Supplier account required.', 'error')
            abort(403)
        return f(*args, **kwargs)
    return decorated


# ── Dashboard ────────────────────────────────────────────────────
@supplier_bp.route('/dashboard')
@supplier_required
def dashboard():
    products = ProductService.get_supplier_products(current_user.id)
    order_data = OrderService.get_supplier_orders(current_user.id)
    
    total_revenue = sum(
        item.quantity * item.unit_price
        for od in order_data if od['order'].status != 'cancelled'
        for item in od['items']
    )

    # Prepare chart data
    status_counts = {}
    for od in order_data:
        status = od['order'].status
        status_counts[status] = status_counts.get(status, 0) + 1
        
    product_revenue = {}
    for od in order_data:
        if od['order'].status != 'cancelled':
            for item in od['items']:
                name = item.product.name
                product_revenue[name] = product_revenue.get(name, 0) + (item.quantity * item.unit_price)
    
    top_products = dict(sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)[:5])

    stats = {
        'total_products': len(products),
        'active_products': sum(1 for p in products if p.is_active),
        'total_orders': len(order_data),
        'pending_orders': status_counts.get('pending', 0),
        'total_revenue': float(total_revenue),
    }
    
    chart_data = {
        'status_labels': list(status_counts.keys()),
        'status_data': list(status_counts.values()),
        'product_labels': list(top_products.keys()),
        'product_revenue': [float(v) for v in top_products.values()]
    }

    return render_template('supplier/dashboard.html', stats=stats, chart_data=chart_data)


# ── Product Management ───────────────────────────────────────────
@supplier_bp.route('/products')
@supplier_required
def products():
    items = ProductService.get_supplier_products(current_user.id)
    return render_template('supplier/products.html', products=items)


@supplier_bp.route('/products/add', methods=['GET', 'POST'])
@supplier_required
def add_product():
    if request.method == 'POST':
        product, error = ProductService.create_product(
            supplier_id=current_user.id,
            name=request.form.get('name', ''),
            description=request.form.get('description', ''),
            price=request.form.get('price', 0),
            stock=request.form.get('stock', 0),
            category=request.form.get('category', ''),
            image_url=request.form.get('image_url', ''),
        )
        if error:
            flash(error, 'error')
            return render_template('supplier/add_product.html')
        flash(f'Product "{product.name}" added!', 'success')
        return redirect(url_for('supplier.products'))
    return render_template('supplier/add_product.html')


@supplier_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@supplier_required
def edit_product(product_id):
    product = ProductService.get_product_by_id(product_id)
    if not product or product.supplier_id != current_user.id:
        flash('Product not found or access denied.', 'error')
        return redirect(url_for('supplier.products'))

    if request.method == 'POST':
        updated, error = ProductService.update_product(
            product_id=product_id,
            supplier_id=current_user.id,
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=request.form.get('price'),
            stock=request.form.get('stock'),
            category=request.form.get('category'),
            image_url=request.form.get('image_url'),
        )
        if error:
            flash(error, 'error')
        else:
            flash('Product updated!', 'success')
        return redirect(url_for('supplier.products'))

    return render_template('supplier/edit_product.html', product=product)


@supplier_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@supplier_required
def delete_product(product_id):
    ok, error = ProductService.delete_product(product_id, current_user.id)
    if not ok:
        flash(error, 'error')
    else:
        flash('Product deactivated.', 'info')
    return redirect(url_for('supplier.products'))


# ── Account Management ─────────────────────────────────────────────
@supplier_bp.route('/account', methods=['GET', 'POST'])
@supplier_required
def account():
    from app.models.supplier_profile import SupplierProfile
    from app import db
    
    profile = SupplierProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = SupplierProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()

    if request.method == 'POST':
        profile.pan_number = request.form.get('pan_number')
        profile.gst_number = request.form.get('gst_number')
        profile.bank_account = request.form.get('bank_account')
        profile.ifsc_code = request.form.get('ifsc_code')
        profile.address = request.form.get('address')
        
        if request.form.get('documents_submitted') == 'on':
            profile.documents_submitted = True
        else:
            profile.documents_submitted = False
            
        # Auto-verification logic
        if profile.pan_number and profile.bank_account and profile.ifsc_code:
            profile.verification_status = 'Verified'
        else:
            profile.verification_status = 'Pending'
            
        db.session.commit()
        flash('Verification details updated successfully!', 'success')
        return redirect(url_for('supplier.account'))

    return render_template('supplier/account.html', profile=profile)

# ── Order Management ─────────────────────────────────────────────
@supplier_bp.route('/orders')
@supplier_required
def orders():
    order_data = OrderService.get_supplier_orders(current_user.id)
    return render_template('supplier/orders.html', order_data=order_data)


@supplier_bp.route('/orders/<int:order_id>')
@supplier_required
def order_detail(order_id):
    order_data = OrderService.get_supplier_orders(current_user.id)
    target = None
    for od in order_data:
        if od['order'].id == order_id:
            target = od
            break
    if not target:
        flash('Order not found.', 'error')
        return redirect(url_for('supplier.orders'))
    return render_template('supplier/order_detail.html',
                           order=target['order'], items=target['items'])


@supplier_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@supplier_required
def update_status(order_id):
    new_status = request.form.get('status', '')
    ok, error = OrderService.update_order_status(order_id, current_user.id, new_status)
    if not ok:
        flash(error, 'error')
    else:
        flash(f'Order #{order_id} status updated to {new_status}.', 'success')
    return redirect(url_for('supplier.order_detail', order_id=order_id))

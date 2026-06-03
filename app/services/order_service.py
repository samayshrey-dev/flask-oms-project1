"""
OrderService – order creation, lifecycle, and tracking.
"""
import logging
from app import db
from app.models.order import Order, OrderItem, ORDER_STATUSES
from app.models.product import Product
from app.services.cart_service import CartService

logger = logging.getLogger(__name__)

# Valid status transitions
STATUS_FLOW = {
    'pending':   'confirmed',
    'confirmed': 'packed',
    'packed':    'shipped',
    'shipped':   'delivered',
}


class OrderService:

    @staticmethod
    def place_order(customer_id, shipping_address):
        """
        Convert the customer's cart into an order.
        Validates stock, decrements inventory, creates OrderItems.
        """
        if not shipping_address or not shipping_address.strip():
            return None, 'Shipping address is required.'

        cart = CartService.get_cart_details(customer_id)
        if not cart or not cart.items:
            return None, 'Your cart is empty.'

        try:
            # Validate stock for every item
            for ci in cart.items:
                product = Product.query.with_for_update().get(ci.product_id)
                if not product or not product.is_active:
                    return None, f'"{ci.product.name}" is no longer available.'
                if product.stock < ci.quantity:
                    return None, (f'Not enough stock for "{product.name}". '
                                  f'Available: {product.stock}')

            # Create order
            order = Order(
                customer_id=customer_id,
                total_amount=cart.total_price,
                shipping_address=shipping_address.strip(),
                status='pending',
            )
            db.session.add(order)
            db.session.flush()

            # Create order items and decrement stock
            for ci in cart.items:
                product = Product.query.get(ci.product_id)
                oi = OrderItem(
                    order_id=order.id,
                    product_id=ci.product_id,
                    supplier_id=product.supplier_id,
                    quantity=ci.quantity,
                    unit_price=product.price,
                )
                db.session.add(oi)
                product.stock -= ci.quantity

            # Clear the cart
            from app.models.cart import CartItem
            CartItem.query.filter_by(cart_id=cart.id).delete()

            db.session.commit()
            logger.info(f'Order #{order.id} placed by customer {customer_id}')
            return order, None

        except Exception as e:
            db.session.rollback()
            logger.error(f'Place order failed: {e}')
            return None, 'Failed to place order. Please try again.'

    @staticmethod
    def get_customer_orders(customer_id, status=None):
        """Get all orders for a customer, newest first. Optional status filter."""
        query = Order.query.filter_by(customer_id=customer_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Order.created_at.desc()).all()

    @staticmethod
    def get_order_detail(order_id, customer_id=None):
        """Get a single order. If customer_id is given, enforce ownership."""
        query = Order.query.filter_by(id=order_id)
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
        return query.first()

    @staticmethod
    def get_supplier_orders(supplier_id):
        """
        Get all orders containing items from this supplier.
        Returns list of (order, [order_items]) tuples.
        """
        order_items = OrderItem.query.filter_by(supplier_id=supplier_id)\
                                     .order_by(OrderItem.id.desc()).all()

        # Group by order
        orders_map = {}
        for oi in order_items:
            if oi.order_id not in orders_map:
                orders_map[oi.order_id] = {
                    'order': oi.order,
                    'items': [],
                }
            orders_map[oi.order_id]['items'].append(oi)

        return list(orders_map.values())

    @staticmethod
    def update_order_status(order_id, supplier_id, new_status, is_customer=False):
        """
        Supplier advances the order status one step at a time.
        Also supports cancellation by both Supplier and Customer.
        """
        order = Order.query.get(order_id)
        if not order:
            return False, 'Order not found.'

        if not is_customer:
            # Verify the supplier has items in this order
            has_items = OrderItem.query.filter_by(
                order_id=order_id, supplier_id=supplier_id
            ).first()
            if not has_items:
                return False, 'You do not have items in this order.'

        if new_status == 'cancelled':
            if order.status in ('shipped', 'delivered'):
                return False, 'Cannot cancel a shipped/delivered order.'
            order.status = 'cancelled'
            db.session.commit()
            return True, None

        # Enforce sequential status flow
        expected_next = STATUS_FLOW.get(order.status)
        if not expected_next:
            return False, f'Order is already {order.status}. No further updates.'
        if new_status != expected_next:
            return False, f'Next valid status is "{expected_next}", not "{new_status}".'

        try:
            order.status = new_status
            db.session.commit()
            logger.info(f'Order #{order.id} status → {new_status}')
            return True, None
        except Exception as e:
            db.session.rollback()
            logger.error(f'Status update failed: {e}')
            return False, 'Failed to update status.'

"""
CartService – persistent cart management.
"""
import logging
from app import db
from app.models.cart import Cart, CartItem
from app.models.product import Product

logger = logging.getLogger(__name__)


class CartService:

    @staticmethod
    def get_or_create_cart(user_id):
        """Get or lazily create a cart for the user."""
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
        return cart

    @staticmethod
    def add_item(user_id, product_id, quantity=1):
        """Add a product to cart or increase quantity if already present."""
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return False, 'Product not available.'
        if quantity < 1:
            return False, 'Quantity must be at least 1.'
        if product.stock < quantity:
            return False, f'Only {product.stock} units available.'

        cart = CartService.get_or_create_cart(user_id)
        item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()

        try:
            if item:
                new_qty = item.quantity + quantity
                if new_qty > product.stock:
                    return False, f'Only {product.stock} units available (you have {item.quantity} in cart).'
                item.quantity = new_qty
            else:
                item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
                db.session.add(item)
            db.session.commit()
            logger.info(f'Cart updated: user={user_id} product={product_id}')
            return True, None
        except Exception as e:
            db.session.rollback()
            logger.error(f'Add to cart failed: {e}')
            return False, 'Failed to update cart.'

    @staticmethod
    def update_quantity(user_id, item_id, quantity):
        """Set the quantity of a cart item."""
        cart = CartService.get_or_create_cart(user_id)
        item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
        if not item:
            return False, 'Item not found in cart.'

        if quantity < 1:
            return CartService.remove_item(user_id, item_id)

        if quantity > item.product.stock:
            return False, f'Only {item.product.stock} units available.'

        try:
            item.quantity = quantity
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            logger.error(f'Update cart quantity failed: {e}')
            return False, 'Failed to update quantity.'

    @staticmethod
    def remove_item(user_id, item_id):
        """Remove an item from the cart."""
        cart = CartService.get_or_create_cart(user_id)
        item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
        if not item:
            return False, 'Item not found in cart.'
        try:
            db.session.delete(item)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            logger.error(f'Remove from cart failed: {e}')
            return False, 'Failed to remove item.'

    @staticmethod
    def clear_cart(user_id):
        """Remove all items from the cart."""
        cart = CartService.get_or_create_cart(user_id)
        try:
            CartItem.query.filter_by(cart_id=cart.id).delete()
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            logger.error(f'Clear cart failed: {e}')
            return False, 'Failed to clear cart.'

    @staticmethod
    def get_cart_details(user_id):
        """Return cart with all items and computed totals."""
        cart = CartService.get_or_create_cart(user_id)
        return cart

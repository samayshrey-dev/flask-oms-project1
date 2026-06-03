"""
Cart and CartItem models.
Each customer has exactly one Cart (1-to-1).
A Cart contains multiple CartItems.
"""
from datetime import datetime, timezone
from app import db


class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    items = db.relationship('CartItem', backref='cart', lazy='joined',
                            cascade='all, delete-orphan')

    @property
    def total_price(self):
        """Calculate total price of all items in the cart."""
        return sum(item.subtotal for item in self.items)

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items)

    def __repr__(self):
        return f'<Cart user={self.user_id} items={len(self.items)}>'


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Prevent duplicate product entries in the same cart
    __table_args__ = (
        db.UniqueConstraint('cart_id', 'product_id', name='uq_cart_product'),
    )

    @property
    def subtotal(self):
        return float(self.product.price) * self.quantity

    def __repr__(self):
        return f'<CartItem product={self.product_id} qty={self.quantity}>'

"""
Order and OrderItem models.
Supports the full order lifecycle:
  pending → confirmed → packed → shipped → delivered
"""
from datetime import datetime, timezone
from app import db


ORDER_STATUSES = ('pending', 'confirmed', 'packed', 'shipped', 'delivered', 'cancelled')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(
        db.Enum(*ORDER_STATUSES, name='order_status'),
        nullable=False, default='pending'
    )
    shipping_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='joined',
                            cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False,
                              cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order #{self.id} status={self.status}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    @property
    def subtotal(self):
        return float(self.unit_price) * self.quantity

    # Relationship to supplier
    supplier = db.relationship('User', foreign_keys=[supplier_id])

    def __repr__(self):
        return f'<OrderItem order={self.order_id} product={self.product_id}>'

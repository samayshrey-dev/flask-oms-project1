"""
Payment model – simulated payment system.
Supports UPI, Card, and COD methods.
"""
from datetime import datetime, timezone
from app import db


PAYMENT_METHODS = ('upi', 'card', 'cod')
PAYMENT_STATUSES = ('pending', 'success', 'failed')


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'),
                         unique=True, nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    method = db.Column(
        db.Enum(*PAYMENT_METHODS, name='payment_method'),
        nullable=False
    )
    status = db.Column(
        db.Enum(*PAYMENT_STATUSES, name='payment_status'),
        nullable=False, default='pending'
    )
    transaction_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Payment order={self.order_id} {self.method} {self.status}>'

"""
PaymentService – simulated payment processing.
"""
import logging
import uuid
from app import db
from app.models.payment import Payment
from app.models.order import Order

logger = logging.getLogger(__name__)


class PaymentService:

    @staticmethod
    def process_payment(order_id, customer_id, method):
        """
        Simulate processing a payment.
        In a real system this would call Stripe/Razorpay etc.
        """
        valid_methods = ('upi', 'card', 'cod')
        if method not in valid_methods:
            return None, f'Invalid payment method. Choose from: {", ".join(valid_methods)}'

        order = Order.query.filter_by(id=order_id, customer_id=customer_id).first()
        if not order:
            return None, 'Order not found.'

        if order.status != 'pending':
            return None, 'Payment can only be made for pending orders.'

        # Check if payment already exists
        existing = Payment.query.filter_by(order_id=order_id).first()
        if existing and existing.status == 'success':
            return None, 'Payment already completed for this order.'

        try:
            # Simulate: all payments succeed except a specific test case
            transaction_id = f'TXN-{uuid.uuid4().hex[:12].upper()}'
            status = 'success'  # In real system, this comes from gateway

            payment = Payment(
                order_id=order_id,
                amount=order.total_amount,
                method=method,
                status=status,
                transaction_id=transaction_id,
            )
            db.session.add(payment)

            # Update order status to confirmed after successful payment
            if status == 'success':
                order.status = 'confirmed'

            db.session.commit()
            logger.info(f'Payment {status} for order #{order_id}: {transaction_id}')
            return payment, None

        except Exception as e:
            db.session.rollback()
            logger.error(f'Payment processing failed: {e}')
            return None, 'Payment processing failed.'

    @staticmethod
    def get_payment_for_order(order_id):
        return Payment.query.filter_by(order_id=order_id).first()

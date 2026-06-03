"""
Seed script – creates sample data for testing.
Run: python seed.py
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart

app = create_app()

SAMPLE_PRODUCTS = [
    {
        'name': 'Wireless Bluetooth Headphones',
        'description': 'Premium noise-cancelling headphones with 30-hour battery life.',
        'price': 2499.00,
        'stock': 50,
        'category': 'Electronics',
    },
    {
        'name': 'USB-C Hub 7-in-1',
        'description': 'Multi-port adapter with HDMI, USB 3.0, SD card reader.',
        'price': 1299.00,
        'stock': 100,
        'category': 'Electronics',
    },
    {
        'name': 'Cotton T-Shirt (Black)',
        'description': '100% organic cotton, comfortable fit, available in all sizes.',
        'price': 499.00,
        'stock': 200,
        'category': 'Clothing',
    },
    {
        'name': 'Running Shoes – Pro',
        'description': 'Lightweight mesh running shoes with cushioned sole.',
        'price': 3999.00,
        'stock': 30,
        'category': 'Footwear',
    },
    {
        'name': 'Stainless Steel Water Bottle',
        'description': 'Double-wall insulated, keeps drinks cold for 24 hours.',
        'price': 699.00,
        'stock': 150,
        'category': 'Home & Kitchen',
    },
    {
        'name': 'Mechanical Keyboard RGB',
        'description': 'Cherry MX Blue switches, full RGB backlighting, 104 keys.',
        'price': 4599.00,
        'stock': 40,
        'category': 'Electronics',
    },
    {
        'name': 'Yoga Mat – Premium',
        'description': 'Non-slip, eco-friendly TPE material, 6mm thick.',
        'price': 899.00,
        'stock': 80,
        'category': 'Fitness',
    },
    {
        'name': 'Notebook – Leather Bound',
        'description': 'A5 hardcover journal, 200 ruled pages, premium finish.',
        'price': 349.00,
        'stock': 300,
        'category': 'Stationery',
    },
]


def seed():
    with app.app_context():
        # Check if data already exists
        if User.query.first():
            print('Database already has data. Skipping seed.')
            return

        print('Seeding database...')

        # Create a supplier
        supplier = User(name='TechMart Supplies', email='supplier@example.com', role='supplier')
        supplier.set_password('password123')
        db.session.add(supplier)

        # Create a second supplier
        supplier2 = User(name='FashionHub', email='supplier2@example.com', role='supplier')
        supplier2.set_password('password123')
        db.session.add(supplier2)

        # Create a customer
        customer = User(name='John Doe', email='customer@example.com', role='customer')
        customer.set_password('password123')
        db.session.add(customer)
        db.session.flush()

        # Create cart for customer
        cart = Cart(user_id=customer.id)
        db.session.add(cart)

        # Create products
        for i, product_data in enumerate(SAMPLE_PRODUCTS):
            sid = supplier.id if i < 5 else supplier2.id
            product = Product(supplier_id=sid, **product_data)
            db.session.add(product)

        db.session.commit()
        print('✅ Seed data created successfully!')
        print()
        print('Test accounts:')
        print('  Customer: customer@example.com / password123')
        print('  Supplier: supplier@example.com / password123')
        print('  Supplier: supplier2@example.com / password123')


if __name__ == '__main__':
    seed()

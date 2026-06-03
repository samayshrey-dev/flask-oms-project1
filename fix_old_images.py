"""
Update images for the original 8 seed products.
Run: python3 fix_old_images.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.product import Product

app = create_app()

IMAGE_MAP = {
    'Wireless Bluetooth Headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80',
    'USB-C Hub 7-in-1': 'https://images.unsplash.com/photo-1625842268584-8f3296236761?auto=format&fit=crop&w=600&q=80',
    'Cotton T-Shirt (Black)': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?auto=format&fit=crop&w=600&q=80',
    'Running Shoes – Pro': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80',
    'Stainless Steel Water Bottle': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=600&q=80',
    'Mechanical Keyboard RGB': 'https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=600&q=80',
    'Yoga Mat – Premium': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&w=600&q=80',
    'Notebook – Leather Bound': 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?auto=format&fit=crop&w=600&q=80',
}

with app.app_context():
    updated = 0
    for name, url in IMAGE_MAP.items():
        product = Product.query.filter_by(name=name).first()
        if product:
            product.image_url = url
            updated += 1
            print(f'  ✅ {name}')
        else:
            print(f'  ⚠️  Not found: {name}')
    db.session.commit()
    print(f'\n🖼️  Updated images for {updated} original products.')

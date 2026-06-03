"""
Seed script – adds 10 products per category with real product images.
Run: python3 seed_products.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.product import Product
from app.models.user import User

app = create_app()

# Curated product images from Unsplash (free, no auth needed)
PRODUCTS = [
    # ── Electronics (10) ────────────────────────────────────────
    {'name': 'Sony WH-1000XM5 Headphones', 'description': 'Industry-leading noise cancellation with 30-hour battery life and premium sound quality.', 'price': 24990.00, 'stock': 45, 'category': 'Electronics', 'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Apple iPad Air M2', 'description': '11-inch Liquid Retina display, M2 chip, 128GB storage with all-day battery life.', 'price': 59900.00, 'stock': 20, 'category': 'Electronics', 'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Samsung 4K Smart TV 55"', 'description': 'Crystal UHD display with HDR10+, Smart Hub, and Alexa built-in.', 'price': 42999.00, 'stock': 15, 'category': 'Electronics', 'image_url': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=600&q=80'},
    {'name': 'JBL Charge 5 Speaker', 'description': 'Portable Bluetooth speaker with powerful bass, IP67 waterproof, 20-hour playtime.', 'price': 12999.00, 'stock': 60, 'category': 'Electronics', 'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Logitech MX Master 3S Mouse', 'description': 'Ergonomic wireless mouse with 8K DPI tracking and USB-C fast charging.', 'price': 8999.00, 'stock': 80, 'category': 'Electronics', 'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Canon EOS R50 Camera', 'description': 'Mirrorless camera with 24.2MP sensor, 4K video recording, and 15fps burst shooting.', 'price': 65999.00, 'stock': 10, 'category': 'Electronics', 'image_url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Apple AirPods Pro 2', 'description': 'Active noise cancellation, spatial audio, MagSafe charging case, 6-hour battery.', 'price': 24900.00, 'stock': 55, 'category': 'Electronics', 'image_url': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Anker 65W USB-C Charger', 'description': 'GaN II technology, compact design, fast charging for laptops and phones.', 'price': 3499.00, 'stock': 120, 'category': 'Electronics', 'image_url': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Samsung Galaxy Watch 6', 'description': 'Advanced health monitoring, sapphire crystal display, 40-hour battery life.', 'price': 26999.00, 'stock': 30, 'category': 'Electronics', 'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Nintendo Switch OLED', 'description': '7-inch OLED screen, 64GB storage, enhanced audio, wide adjustable stand.', 'price': 29999.00, 'stock': 25, 'category': 'Electronics', 'image_url': 'https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?auto=format&fit=crop&w=600&q=80'},

    # ── Clothing (10) ───────────────────────────────────────────
    {'name': 'Levi\'s 501 Original Jeans', 'description': 'Classic straight-leg fit in premium dark indigo wash denim.', 'price': 3999.00, 'stock': 100, 'category': 'Clothing', 'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Oversized Hoodie – Charcoal', 'description': 'Ultra-soft fleece-lined hoodie with kangaroo pocket, relaxed fit.', 'price': 1999.00, 'stock': 150, 'category': 'Clothing', 'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Polo Ralph Lauren T-Shirt', 'description': 'Classic fit cotton tee with signature pony logo, breathable fabric.', 'price': 2499.00, 'stock': 200, 'category': 'Clothing', 'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Bomber Jacket – Olive Green', 'description': 'Lightweight nylon shell with ribbed cuffs and hem, zip-front closure.', 'price': 4999.00, 'stock': 50, 'category': 'Clothing', 'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Formal Slim Fit Shirt – White', 'description': 'Premium cotton dress shirt with spread collar and French cuffs.', 'price': 1799.00, 'stock': 120, 'category': 'Clothing', 'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Chinos – Khaki Stretch', 'description': 'Slim-fit stretch cotton chinos with hidden comfort waistband.', 'price': 2299.00, 'stock': 90, 'category': 'Clothing', 'image_url': 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Denim Jacket – Classic Blue', 'description': 'Vintage-wash trucker jacket with chest pockets and button closure.', 'price': 3499.00, 'stock': 60, 'category': 'Clothing', 'image_url': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Wool Blend Sweater – Navy', 'description': 'Crew-neck sweater in soft wool-cashmere blend, rib-knit trim.', 'price': 2799.00, 'stock': 70, 'category': 'Clothing', 'image_url': 'https://images.unsplash.com/photo-1434389677669-e08b4cda3a0a?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Linen Summer Shorts', 'description': 'Breathable linen-cotton blend shorts with drawstring waist.', 'price': 1499.00, 'stock': 110, 'category': 'Clothing', 'image_url': 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Athletic Track Pants', 'description': 'Moisture-wicking fabric with tapered fit and zippered pockets.', 'price': 1899.00, 'stock': 130, 'category': 'Clothing', 'image_url': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?auto=format&fit=crop&w=600&q=80'},

    # ── Footwear (10) ───────────────────────────────────────────
    {'name': 'Nike Air Max 270', 'description': 'Lifestyle sneakers with Max Air unit for all-day comfort and style.', 'price': 12995.00, 'stock': 40, 'category': 'Footwear', 'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Adidas Ultraboost 23', 'description': 'Responsive BOOST midsole with Primeknit+ upper for premium running.', 'price': 16999.00, 'stock': 35, 'category': 'Footwear', 'image_url': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Converse Chuck Taylor All Star', 'description': 'Classic canvas high-top sneakers with vulcanized rubber sole.', 'price': 4499.00, 'stock': 80, 'category': 'Footwear', 'image_url': 'https://images.unsplash.com/photo-1607522370275-f14206abe5d3?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Puma RS-X Reinvention', 'description': 'Retro-inspired chunky sneakers with running system technology.', 'price': 8999.00, 'stock': 50, 'category': 'Footwear', 'image_url': 'https://images.unsplash.com/photo-1600269452121-4f2416e55c28?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Timberland 6-Inch Boots', 'description': 'Waterproof leather boots with padded collar and lug sole.', 'price': 15999.00, 'stock': 25, 'category': 'Footwear', 'image_url': 'https://images.unsplash.com/photo-1520639888713-7851133b1ed0?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Vans Old Skool – Black/White', 'description': 'Iconic side-stripe skate shoes with durable suede and canvas upper.', 'price': 5499.00, 'stock': 70, 'category': 'Footwear', 'image_url': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=600&q=80'},
    {'name': 'New Balance 574 Classic', 'description': 'Heritage running shoes with ENCAP midsole cushioning.', 'price': 7999.00, 'stock': 45, 'category': 'Footwear', 'image_url': 'https://images.unsplash.com/photo-1539185441755-769473a23570?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Formal Oxford Shoes – Brown', 'description': 'Genuine leather Oxfords with Goodyear welt construction.', 'price': 6999.00, 'stock': 30, 'category': 'Footwear', 'image_url': 'https://images.unsplash.com/photo-1614252369475-531eba835eb1?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Birkenstock Arizona Sandals', 'description': 'Iconic two-strap sandals with contoured cork-latex footbed.', 'price': 8499.00, 'stock': 55, 'category': 'Footwear', 'image_url': 'https://images.unsplash.com/photo-1603487742131-4160ec999306?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Reebok Classic Leather', 'description': 'Retro leather sneakers with die-cut EVA midsole for lightweight comfort.', 'price': 6499.00, 'stock': 65, 'category': 'Footwear', 'image_url': 'https://images.unsplash.com/photo-1491553895911-0055eca6402d?auto=format&fit=crop&w=600&q=80'},

    # ── Home & Kitchen (10) ─────────────────────────────────────
    {'name': 'Instant Pot Duo 7-in-1', 'description': 'Electric pressure cooker, slow cooker, rice cooker – all in one, 6-quart.', 'price': 8999.00, 'stock': 40, 'category': 'Home & Kitchen', 'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Dyson V15 Detect Vacuum', 'description': 'Cordless vacuum with laser dust detection and HEPA filtration.', 'price': 52999.00, 'stock': 15, 'category': 'Home & Kitchen', 'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85f82e?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Le Creuset Dutch Oven 5.5Qt', 'description': 'Enameled cast iron, superior heat retention, oven safe to 500°F.', 'price': 14999.00, 'stock': 20, 'category': 'Home & Kitchen', 'image_url': 'https://images.unsplash.com/photo-1585515320310-259814833e62?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Philips Air Fryer XXL', 'description': 'Rapid air technology for crispy food with 90% less fat, 7.3L capacity.', 'price': 12999.00, 'stock': 35, 'category': 'Home & Kitchen', 'image_url': 'https://images.unsplash.com/photo-1648733966427-0e0f6aab0e4e?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Nespresso Vertuo Coffee Machine', 'description': 'One-touch brewing with centrifusion technology, 5 cup sizes.', 'price': 15999.00, 'stock': 25, 'category': 'Home & Kitchen', 'image_url': 'https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Himalayan Pink Salt Lamp', 'description': 'Hand-carved crystal lamp with warm amber glow, wooden base.', 'price': 1299.00, 'stock': 100, 'category': 'Home & Kitchen', 'image_url': 'https://images.unsplash.com/photo-1600166898405-da9535204843?auto=format&fit=crop&w=600&q=80'},
    {'name': 'KitchenAid Stand Mixer', 'description': 'Tilt-head stand mixer with 10 speeds, 4.5-quart stainless bowl.', 'price': 29999.00, 'stock': 12, 'category': 'Home & Kitchen', 'image_url': 'https://images.unsplash.com/photo-1594834749740-74b3f6764be4?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Scented Soy Candle Set (6-Pack)', 'description': 'Hand-poured soy wax candles in lavender, vanilla, citrus, and more.', 'price': 1799.00, 'stock': 200, 'category': 'Home & Kitchen', 'image_url': 'https://images.unsplash.com/photo-1602607441273-54a3835c8d7d?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Bamboo Cutting Board Set', 'description': 'Set of 3 organic bamboo boards with juice groove and easy-grip handles.', 'price': 999.00, 'stock': 150, 'category': 'Home & Kitchen', 'image_url': 'https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Smart LED Strip Lights 10m', 'description': 'WiFi-enabled RGB strip with app control, voice assistant compatible.', 'price': 1499.00, 'stock': 180, 'category': 'Home & Kitchen', 'image_url': 'https://images.unsplash.com/photo-1558171813-4c088753af8f?auto=format&fit=crop&w=600&q=80'},

    # ── Fitness (10) ────────────────────────────────────────────
    {'name': 'Bowflex Adjustable Dumbbells', 'description': 'Adjustable from 5-52.5 lbs each, replaces 15 sets of weights.', 'price': 32999.00, 'stock': 18, 'category': 'Fitness', 'image_url': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Resistance Band Set (5-Pack)', 'description': 'Latex-free bands in 5 resistance levels with door anchor and handles.', 'price': 1299.00, 'stock': 200, 'category': 'Fitness', 'image_url': 'https://images.unsplash.com/photo-1598289431512-b97b0917affc?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Fitbit Charge 6 Tracker', 'description': 'Advanced fitness tracker with GPS, heart rate, sleep tracking, 7-day battery.', 'price': 14999.00, 'stock': 50, 'category': 'Fitness', 'image_url': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?auto=format&fit=crop&w=600&q=80'},
    {'name': 'TRX Suspension Trainer Pro', 'description': 'Military-grade suspension training system for full-body workouts.', 'price': 8999.00, 'stock': 30, 'category': 'Fitness', 'image_url': 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Foam Roller – High Density', 'description': 'Extra-firm EVA foam roller for deep tissue massage, 36-inch.', 'price': 899.00, 'stock': 150, 'category': 'Fitness', 'image_url': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Jump Rope – Speed Pro', 'description': 'Weighted speed rope with ball bearings and adjustable steel cable.', 'price': 699.00, 'stock': 180, 'category': 'Fitness', 'image_url': 'https://images.unsplash.com/photo-1601422407692-ec4eeec1d9b3?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Pull-Up Bar – Doorway Mount', 'description': 'Heavy-duty steel pull-up bar with foam grips, fits doors 24-36 inches.', 'price': 2499.00, 'stock': 60, 'category': 'Fitness', 'image_url': 'https://images.unsplash.com/photo-1540497077202-7c8a3999166f?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Kettlebell – Cast Iron 16kg', 'description': 'Solid cast iron with wide grip handle and flat bottom for stability.', 'price': 2999.00, 'stock': 45, 'category': 'Fitness', 'image_url': 'https://images.unsplash.com/photo-1517963879433-6ad2b056d712?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Gym Bag – Duffle XL', 'description': 'Waterproof nylon duffle with shoe compartment and wet pocket.', 'price': 1799.00, 'stock': 90, 'category': 'Fitness', 'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Protein Shaker Bottle 700ml', 'description': 'BPA-free blender bottle with stainless steel mixing ball.', 'price': 499.00, 'stock': 250, 'category': 'Fitness', 'image_url': 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=600&q=80'},

    # ── Stationery (10) ─────────────────────────────────────────
    {'name': 'Moleskine Classic Notebook', 'description': 'Hardcover A5 ruled notebook with ivory-coloured paper, 240 pages.', 'price': 1599.00, 'stock': 120, 'category': 'Stationery', 'image_url': 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Staedtler Triplus Fineliner Set', 'description': 'Set of 20 vibrant colours in ergonomic triangular barrel.', 'price': 899.00, 'stock': 200, 'category': 'Stationery', 'image_url': 'https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Parker Jotter Ballpoint Pen', 'description': 'Stainless steel pen with click mechanism and QuinkFlow ink refill.', 'price': 699.00, 'stock': 300, 'category': 'Stationery', 'image_url': 'https://images.unsplash.com/photo-1585336261022-680e295ce3fe?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Desk Organiser – Bamboo', 'description': 'Multi-compartment bamboo desk caddy for pens, phone, and supplies.', 'price': 1299.00, 'stock': 80, 'category': 'Stationery', 'image_url': 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Sticky Notes Pastel Pack (12)', 'description': '3x3 inch sticky notes in 12 pastel colours, 100 sheets each.', 'price': 349.00, 'stock': 500, 'category': 'Stationery', 'image_url': 'https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Washi Tape Collection (20 Rolls)', 'description': 'Decorative Japanese masking tape in assorted patterns and widths.', 'price': 599.00, 'stock': 150, 'category': 'Stationery', 'image_url': 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Whiteboard Markers (Set of 8)', 'description': 'Chisel-tip dry erase markers in 8 colours with low-odour ink.', 'price': 449.00, 'stock': 200, 'category': 'Stationery', 'image_url': 'https://images.unsplash.com/photo-1568205631919-18933a040f65?auto=format&fit=crop&w=600&q=80'},
    {'name': 'A4 Sketchbook – 200gsm', 'description': 'Spiral-bound sketchbook with heavyweight acid-free paper, 60 sheets.', 'price': 799.00, 'stock': 100, 'category': 'Stationery', 'image_url': 'https://images.unsplash.com/photo-1456735190827-d1262f71b8a3?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Mechanical Pencil Set – Rotring', 'description': 'Professional drafting pencils in 0.3mm, 0.5mm, and 0.7mm sizes.', 'price': 1899.00, 'stock': 70, 'category': 'Stationery', 'image_url': 'https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?auto=format&fit=crop&w=600&q=80'},
    {'name': 'Planner 2025 – Weekly Layout', 'description': 'Premium hardcover planner with weekly spread, goal pages, and ribbon markers.', 'price': 1199.00, 'stock': 90, 'category': 'Stationery', 'image_url': 'https://images.unsplash.com/photo-1506784365847-bbad939e9335?auto=format&fit=crop&w=600&q=80'},
]


def seed_products():
    with app.app_context():
        # Get a supplier to assign products to
        supplier = User.query.filter_by(role='supplier').first()
        if not supplier:
            print('❌ No supplier found. Run seed.py first.')
            return

        suppliers = User.query.filter_by(role='supplier').all()
        
        added = 0
        for i, p in enumerate(PRODUCTS):
            # Check if product already exists
            existing = Product.query.filter_by(name=p['name']).first()
            if existing:
                # Update image if missing
                if not existing.image_url:
                    existing.image_url = p['image_url']
                    added += 1
                continue
            
            # Alternate between suppliers
            sid = suppliers[i % len(suppliers)].id
            product = Product(supplier_id=sid, **p)
            db.session.add(product)
            added += 1

        db.session.commit()
        
        total = Product.query.count()
        cats = db.session.query(Product.category).distinct().all()
        
        print(f'✅ Added {added} new products!')
        print(f'📦 Total products in database: {total}')
        print(f'📂 Categories: {", ".join([c[0] for c in cats])}')


if __name__ == '__main__':
    seed_products()

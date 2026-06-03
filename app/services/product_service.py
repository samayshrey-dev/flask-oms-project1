"""
ProductService – product CRUD and search logic.
"""
import logging
from app import db
from app.models.product import Product

logger = logging.getLogger(__name__)


class ProductService:

    @staticmethod
    def create_product(supplier_id, name, description, price, stock,
                       category=None, image_url=None):
        """Create a new product for a supplier."""
        if not name or price is None or stock is None:
            return None, 'Name, price, and stock are required.'
        if float(price) < 0:
            return None, 'Price cannot be negative.'
        if int(stock) < 0:
            return None, 'Stock cannot be negative.'

        try:
            product = Product(
                name=name.strip(),
                description=description.strip() if description else None,
                price=float(price),
                stock=int(stock),
                category=category.strip() if category else None,
                image_url=image_url.strip() if image_url else None,
                supplier_id=supplier_id,
            )
            db.session.add(product)
            db.session.commit()
            logger.info(f'Product created: {product.name} by supplier {supplier_id}')
            return product, None
        except Exception as e:
            db.session.rollback()
            logger.error(f'Create product failed: {e}')
            return None, 'Failed to create product.'

    @staticmethod
    def update_product(product_id, supplier_id, **kwargs):
        """Update a product owned by the supplier."""
        product = Product.query.filter_by(id=product_id, supplier_id=supplier_id).first()
        if not product:
            return None, 'Product not found or access denied.'

        allowed = ('name', 'description', 'price', 'stock', 'category',
                    'image_url', 'is_active')
        try:
            for key, value in kwargs.items():
                if key in allowed and value is not None:
                    if key == 'price' and float(value) < 0:
                        return None, 'Price cannot be negative.'
                    if key == 'stock' and int(value) < 0:
                        return None, 'Stock cannot be negative.'
                    setattr(product, key, value)
            db.session.commit()
            logger.info(f'Product updated: {product.id}')
            return product, None
        except Exception as e:
            db.session.rollback()
            logger.error(f'Update product failed: {e}')
            return None, 'Failed to update product.'

    @staticmethod
    def delete_product(product_id, supplier_id):
        """Soft-delete a product by marking it inactive."""
        product = Product.query.filter_by(id=product_id, supplier_id=supplier_id).first()
        if not product:
            return False, 'Product not found or access denied.'
        try:
            product.is_active = False
            db.session.commit()
            logger.info(f'Product deactivated: {product.id}')
            return True, None
        except Exception as e:
            db.session.rollback()
            logger.error(f'Delete product failed: {e}')
            return False, 'Failed to delete product.'

    @staticmethod
    def get_supplier_products(supplier_id):
        """Get all products for a supplier (including inactive)."""
        return Product.query.filter_by(supplier_id=supplier_id)\
                            .order_by(Product.created_at.desc()).all()

    @staticmethod
    def get_active_products(search=None, category=None):
        """Get all active products, optionally filtered by search/category."""
        query = Product.query.filter_by(is_active=True)

        if search:
            search_term = f'%{search.strip()}%'
            query = query.filter(
                db.or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                )
            )

        if category:
            query = query.filter_by(category=category)

        return query.filter(Product.stock > 0)\
                    .order_by(Product.created_at.desc()).all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def get_categories():
        """Return distinct categories."""
        rows = db.session.query(Product.category)\
                         .filter(Product.is_active == True, Product.category.isnot(None))\
                         .distinct().all()
        return [r[0] for r in rows if r[0]]

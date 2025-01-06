from flask import Flask
from extensions import db
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.user import User
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def init_db():
    app = create_app()
    with app.app_context():
        # Remove old database
        if os.path.exists('app.db'):
            os.remove('app.db')
            
        # Create tables
        db.create_all()
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        db.session.add(admin_user)
        db.session.commit()
        
        # Add sample products
        products = [
            Product(
                name='Gaming Mouse',
                description='High-precision gaming mouse with RGB lighting',
                price=59.99
            ),
            Product(
                name='Mechanical Keyboard',
                description='RGB mechanical keyboard with Cherry MX switches',
                price=129.99
            ),
            Product(
                name='Gaming Headset',
                description='7.1 surround sound gaming headset',
                price=89.99
            )
        ]
        
        # Add products to database
        for product in products:
            db.session.add(product)
        
        # Commit changes
        db.session.commit()
        print("Database initialized with sample products")
        
        # Print out the products to verify
        print("\nVerifying products in database:")
        for product in Product.query.all():
            print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price:.2f}")

if __name__ == '__main__':
    init_db()

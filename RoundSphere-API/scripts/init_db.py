import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from extensions import db
from models.user import User
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.payment import Payment
from models.iot_device import IoTDevice
from models.measurement_data import MeasurementData
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def init_db():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                password='admin123'  # Change this in production!
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_db()

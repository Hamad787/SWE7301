from flask import Flask
from flask_migrate import Migrate
from extensions import db
from config import Config

# Import all models
from models.user import User
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.payment import Payment
from models.iot_device import IoTDevice
from models.measurement_data import MeasurementData

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()

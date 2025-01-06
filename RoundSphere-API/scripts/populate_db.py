from app import create_app
from models.product import Product
from models.order import Order
from extensions import db
from decimal import Decimal

def reset_and_populate():
    app = create_app()
    with app.app_context():
        # Delete existing entries
        Product.query.delete()
        Order.query.delete()
        db.session.commit()

        # Define products and subscription packages
        products = [
            {
                'name': 'EcoShade Pro Balls - Standard Pack',
                'description': 'Premium UV-resistant shade balls for small to medium reservoirs. Pack of 1000 units. Features:\n'
                             '• High-density polyethylene construction\n'
                             '• 4-inch diameter for optimal coverage\n'
                             '• UV-resistant black coating\n'
                             '• Reduces evaporation by up to 90%\n'
                             '• Prevents algae growth',
                'price': 499.99
            },
            {
                'name': 'EcoShade Pro Balls - Industrial Pack',
                'description': 'Bulk package of 10,000 shade balls for large-scale implementations. Ideal for industrial reservoirs.\n'
                             '• Bulk savings of 15%\n'
                             '• Free shipping included\n'
                             '• Installation guide included\n'
                             '• Technical support available',
                'price': 4499.99
            },
            {
                'name': 'SmartSphere IoT Monitoring Pack',
                'description': 'Smart shade balls with integrated IoT sensors. Pack of 100 units.\n'
                             '• Real-time temperature monitoring\n'
                             '• Humidity sensors\n'
                             '• Solar-powered operation\n'
                             '• 5-year battery life\n'
                             '• Wireless data transmission',
                'price': 1999.99
            },
            {
                'name': 'Basic Data Access Subscription - Monthly',
                'description': 'Monthly access to raw data collected from IoT-enabled shade balls.\n'
                             '• Raw temperature and humidity data\n'
                             '• Daily data updates\n'
                             '• Basic API access\n'
                             '• Email support\n'
                             '• Up to 1000 API calls per day',
                'price': 99.99
            },
            {
                'name': 'Professional Data Access Subscription - Monthly',
                'description': 'Advanced monthly subscription for processed data and analytics.\n'
                             '• Real-time data access\n'
                             '• Processed and cleaned datasets\n'
                             '• Advanced analytics dashboard\n'
                             '• Unlimited API calls\n'
                             '• Priority technical support\n'
                             '• Custom data export formats',
                'price': 299.99
            },
            {
                'name': 'Enterprise Data Lake Access - Annual',
                'description': 'Annual enterprise-level access to complete data lake and analytics tools.\n'
                             '• Full data lake access\n'
                             '• Machine learning ready datasets\n'
                             '• Custom API integration\n'
                             '• Dedicated support team\n'
                             '• Quarterly trend analysis reports\n'
                             '• White-label options available',
                'price': 9999.99
            }
        ]

        # Create products
        for product_data in products:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price']
            )
            db.session.add(product)

        db.session.commit()
        print("Flask API database reset and populated with new products successfully!")

if __name__ == '__main__':
    reset_and_populate()

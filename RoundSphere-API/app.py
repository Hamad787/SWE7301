from flask import Flask, jsonify
from extensions import db, jwt, migrate  # Import the extensions from extensions.py
from config import Config
from flask_restx import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize API
api = Api(app, version='1.0', title='RoundSphere API',
          description='API for managing products, orders, and payment operations.')

# Load configuration from config.py
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

# Register Swagger UI
SWAGGER_URL = '/swagger-ui'  # Swagger UI static files will be served from this endpoint
API_URL = '/swagger.json'  # The endpoint for the Swagger JSON file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "RoundSphere API"}
)

# Register the Swagger UI blueprint with the Flask app
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Serve the swagger.json file (this should work properly now)
@app.route('/swagger.json')
def swagger_json():
    return jsonify(api.__schema__)

# Optional: Add Swagger documentation for the API at the '/swagger-ui' endpoint
api.documentation = '/swagger-ui'

# Start the Flask application
if __name__ == '__main__':
    # Import views AFTER the api initialization to avoid circular imports
    from views.product_views import ProductViewSet
    from views.order_views import OrderViewSet
    from views.measurement_views import MeasurementDataView
    from views.payment_views import PaymentView
    from views.login_views import LoginView

    # Define the routes
    api.add_resource(ProductViewSet, '/api/products', '/api/products/<int:product_id>')
    api.add_resource(OrderViewSet, '/api/orders', '/api/orders/<int:order_id>')
    api.add_resource(MeasurementDataView, '/api/data')
    api.add_resource(PaymentView, '/api/order/<int:order_id>/payment')
    api.add_resource(LoginView, '/api/login')

    app.run(host='0.0.0.0', port=5000, debug=True)

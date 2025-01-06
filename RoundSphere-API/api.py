from flask_restx import Api

# Initialize API with Swagger documentation
api = Api(
    version='1.0',
    title='RoundSphere API',
    description='API for managing products, orders, and payment operations',
    doc='/api/docs',  # Swagger UI will be available at /api/docs
    prefix='/api'  # All routes will be prefixed with /api
)

# Create namespaces for API organization
ns_products = api.namespace('products', description='Product operations')
ns_orders = api.namespace('orders', description='Order operations')
ns_data = api.namespace('data', description='Measurement data operations')
ns_payment = api.namespace('payment', description='Payment operations')
ns_auth = api.namespace('auth', description='Authentication operations')

# Import views
from views.product_views import ProductList, ProductDetail
from views.order_views import OrderViewSet
from views.measurement_views import MeasurementDataView
from views.payment_views import PaymentView
from views.login_views import LoginView

# Define the routes with their respective namespaces
ns_products.add_resource(ProductList, '/')
ns_products.add_resource(ProductDetail, '/<int:product_id>')
ns_orders.add_resource(OrderViewSet, '/', '/<int:order_id>')
ns_data.add_resource(MeasurementDataView, '/')
ns_payment.add_resource(PaymentView, '/order/<int:order_id>')
ns_auth.add_resource(LoginView, '/login')

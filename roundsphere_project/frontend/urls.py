from django.urls import path
from .views import ProductViewSet, OrderViewSet, MeasurementDataView, PaymentView
from frontend.views import get_flask_data, home, order_list, login_view, add_product

urlpatterns = [
    path('flask-data/', get_flask_data, name='flask_data'),
    path('login/', login_view, name='login'),
    path('products/', home, name='product-list'),
    path('products/add/', add_product, name='add-product'),
    path('products/<int:product_id>/', ProductViewSet.as_view(), name='product-detail'),
    path('orders/', OrderViewSet.as_view(), name='order-list'),
    path('orders/<int:order_id>/', OrderViewSet.as_view(), name='order-detail'),
    path('data/', MeasurementDataView.as_view(), name='measurement-list'),
    path('order/<int:order_id>/payment', PaymentView.as_view(), name='payment-create'),
    path('', login_view, name='login'),
    path('orders/', order_list, name='order_list'),
]

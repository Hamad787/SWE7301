from django.urls import path
from .views import (
    ProductViewSet, 
    OrderViewSet, 
    MeasurementDataView, 
    PaymentView,
    login_view,
    home,
    add_product,
    order_list,
    order_payment,
    process_payment,
    create_order,
    get_payment_status
)

app_name = 'frontend'  

urlpatterns = [
    # Authentication
    path('', login_view, name='login'),
    
    # Frontend views
    path('home/', home, name='home'),
    path('products/add/', add_product, name='add_product'),
    path('orders/', order_list, name='orders'),
    path('orders/<int:order_id>/payment/', order_payment, name='order_payment'),
    path('orders/<int:order_id>/process-payment/', process_payment, name='process_payment'),
    path('orders/<int:order_id>/payment-status/', get_payment_status, name='payment_status'),
    path('products/<int:product_id>/create-order/', create_order, name='create_order'),
    
    # API endpoints
    path('api/products/', ProductViewSet.as_view(), name='api_products'),
    path('api/products/<int:product_id>/', ProductViewSet.as_view(), name='api_product_detail'),
    path('api/orders/', OrderViewSet.as_view(), name='api_orders'),
    path('api/orders/<int:order_id>/', OrderViewSet.as_view(), name='api_order_detail'),
    path('api/orders/<int:order_id>/payment/', PaymentView.as_view(), name='api_payment'),
    path('api/measurements/', MeasurementDataView.as_view(), name='api_measurements'),
]

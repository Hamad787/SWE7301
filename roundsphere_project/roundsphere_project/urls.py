from django.contrib import admin
from django.urls import path, include
from frontend.views import get_flask_data

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('flask-data/', include('frontend.urls')),  # Include the frontend app's URLs
    # path('flask-data/', get_flask_data, name='flask_data'),
    path('', include('frontend.urls')), 
]

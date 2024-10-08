from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView  # Correct import here
from .views import root_route, logout_route

# Schema view setup for Swagger and Redoc API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Cheshire Captures API",
        default_version='v1',
        description="API documentation for Cheshire Captures",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Root route and admin panel
    path('', root_route),  # Handle root route
    path('admin/', admin.site.urls),  # Django admin

    # REST framework authentication
    path('api-auth/', include('rest_framework.urls')), 

    # Logout route for dj-rest-auth
    path('dj-rest-auth/logout/', logout_route),

    # dj-rest-auth endpoints including JWT refresh
    path('dj-rest-auth/', include('dj_rest_auth.urls')), 
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')), 
    path('dj-rest-auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 

    # API-specific routes (ensure you have the urls.py in these apps)
    path('api/photographers/', include('photographers.urls')),  # Photographer-related API
    path('api/photos/', include('photo.urls')),  # Photo-related API
    path('api/messages/', include('messaging.urls')),  # Messaging-related API

    # Swagger and Redoc API documentation
    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

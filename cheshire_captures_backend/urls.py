from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
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
    path('', root_route, name='root'),  # Handle root route
    path('admin/', admin.site.urls),  # Django admin

    # REST framework authentication
    path('api-auth/', include('rest_framework.urls')),

    # Logout route for dj-rest-auth
    path('dj-rest-auth/logout/', logout_route, name='logout'),

    # dj-rest-auth endpoints including JWT refresh
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path(
        'dj-rest-auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),

    # API-specific routes (ensure you have the urls.py in these apps)
    # Photographer-related API
    path('api/photographers/', include('photographers.urls')),
    path('api/photos/', include('photo.urls')),  # Photo-related API

    # Swagger and Redoc API documentation
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]

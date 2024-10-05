from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import root_route, logout_route

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
    path('', root_route),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), 
    path('dj-rest-auth/logout/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')), 
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')), 
    
    # App-specific API routes
    path('', include('photographers.urls')),
    path('api/photos/', include('photo.urls')),
    path('api/messages/', include('messaging.urls')),
    
    # Swagger and Redoc API documentation
    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('photographers.urls')),
    path('auth/', include('dj_rest_auth.urls')), 
    path('', include('photographers.urls')),
]

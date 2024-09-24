from django.contrib import admin
from django.urls import path, include
from cheshire_captures_backend.views import root_route 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('photographers.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('', root_route, name='root'), 
]

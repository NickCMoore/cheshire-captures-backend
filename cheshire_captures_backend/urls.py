from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to Cheshire Captures!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('photographers.urls')),
    path('auth/', include('dj_rest_auth.urls')), 
    path('', home_view),
]

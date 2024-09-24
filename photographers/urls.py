from django.urls import path
from .views import PhotographerList

urlpatterns = [
    path('photographers/', PhotographerList.as_view(), name='photographer-list'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('photographers/', views.PhotographerList.as_view(), name='photographer-list'),
]

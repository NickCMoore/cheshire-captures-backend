from django.urls import path
from photographers import views

urlpatterns = [
    path('photographers/', views.PhotographerList.as_view(), name='photographer-list'),
]

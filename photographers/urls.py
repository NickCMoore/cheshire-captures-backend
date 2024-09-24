from django.urls import path
from .views import PhotographerListCreate, PhotographerDetail

urlpatterns = [
    path('', PhotographerList.as_view(), name='photographer-list'),
    path('<int:pk>/', PhotographerDetail.as_view(), name='photographer-detail'),
]

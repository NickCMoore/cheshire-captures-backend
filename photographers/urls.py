from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhotographerViewSet, FollowViewSet, TopPhotographersView

router = DefaultRouter()
router.register(r'photographers', PhotographerViewSet, basename='photographer')
router.register(r'follows', FollowViewSet, basename='follows')

urlpatterns = [
    path('', include(router.urls)),
    path('top-photographers/', TopPhotographersView.as_view(), name='top-photographers'), 
]

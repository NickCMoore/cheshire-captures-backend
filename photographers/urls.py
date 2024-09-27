from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhotographerViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'photographers', PhotographerViewSet, basename='photographer')
router.register(r'follows', FollowViewSet, basename='follows')

urlpatterns = [
    path('', include(router.urls)),
]

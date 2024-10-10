from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhotographerDetail, PhotographerList, FollowViewSet, TopPhotographersView

router = DefaultRouter()
router.register(r'follows', FollowViewSet, basename='follow')

urlpatterns = [
    path('photographers/', PhotographerList.as_view(), name='photographer-list'),
    path('photographers/top/', TopPhotographersView.as_view(), name='top-photographers'),
    path('photographers/<int:pk>/', PhotographerDetail.as_view(), name='photographer-detail'),
    path('photographers/<int:pk>/follow/', PhotographerDetail.as_view({'post': 'follow'}), name='photographer-follow'),
    path('photographers/<int:pk>/unfollow/', PhotographerDetail.as_view({'post': 'unfollow'}), name='photographer-unfollow'),
    path('', include(router.urls)),
]

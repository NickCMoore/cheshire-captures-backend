from django.urls import path
from .views import PhotographerList, PhotographerDetail, follow_photographer, PhotographerViewSet

urlpatterns = [
    path('photographers/', PhotographerList.as_view(), name='photographer-list'),
    path('photographers/<int:pk>/', PhotographerDetail.as_view(), name='photographer-detail'),
    path('photographers/<int:pk>/follow/', follow_photographer, name='photographer-follow'),
    path('photographers/<int:pk>/unfollow/', PhotographerViewSet.as_view({'post': 'unfollow'}), name='photographer-unfollow'),
]

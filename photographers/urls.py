from django.urls import path
from .views import (
    PhotographerList,
    PhotographerDetail,
    FollowPhotographerView,
    TopPhotographersView,
    PhotographerFollowersAPIView,
)

urlpatterns = [
    path(
        'photographers/',
        PhotographerList.as_view(),
        name='photographer-list'
    ),
    path(
        'photographers/<int:pk>/',
        PhotographerDetail.as_view(),
        name='photographer-detail'
    ),
    path(
        'photographers/<int:pk>/follow/',
        FollowPhotographerView.as_view(),
        name='photographer-follow'
    ),
    path(
        'photographers/<int:pk>/unfollow/',
        FollowPhotographerView.as_view(),
        name='photographer-unfollow'
    ),
    path(
        'top-photographers/',
        TopPhotographersView.as_view(),
        name='top-photographers'
    ),
    path(
        'photographers/<int:pk>/followers/',
        PhotographerFollowersAPIView.as_view(),
        name='photographer-followers'
    ),
]

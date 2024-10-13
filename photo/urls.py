from django.urls import path
from .views import (
    PhotoListCreateView, PhotoDetailView, MyPhotosListView, TopRatedPhotosView,
    rate_photo, PhotoRatingsView, TagListCreateView, LikeListCreateView, CommentListCreateView
)

urlpatterns = [
    path('photos/', PhotoListCreateView.as_view(), name='photo-list'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('photos/my_photos/', MyPhotosListView.as_view(), name='my-photos'),
    path('photos/top-rated/', TopRatedPhotosView.as_view(), name='top-rated-photos'),
    path('photos/<int:pk>/rate/', rate_photo, name='photo-rate'),
    path('photos/<int:pk>/ratings/', PhotoRatingsView.as_view(), name='photo-ratings'),
    path('tags/', TagListCreateView.as_view(), name='tag-list'),
    path('photos/<int:pk>/comments/', CommentListCreateView.as_view(), name='photo-comments'),  
    path('likes/', LikeListCreateView.as_view(), name='like-list'),
]

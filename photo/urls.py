from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhotoViewSet, TagViewSet, LikeViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'photos', PhotoViewSet, basename='photo')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('photos/<int:pk>/like/', PhotoViewSet.as_view({'post': 'like_photo'}), name='photo-like'),
    path('photos/<int:pk>/unlike/', PhotoViewSet.as_view({'post': 'unlike_photo'}), name='photo-unlike'),
    path('photos/<int:pk>/rate/', PhotoViewSet.as_view({'post': 'rate_photo'}), name='photo-rate'), 
    path('photos/top-rated/', PhotoViewSet.as_view({'get': 'top_rated'}), name='photo-top-rated'),
    path('photos/my_photos/', PhotoViewSet.as_view({'get': 'my_photos'}), name='my-photos'),
    path('photos/<int:pk>/comments/', CommentViewSet.as_view({'post': 'create'}), name='photo-add-comment'),
    path('photos/<int:pk>/ratings/', PhotoViewSet.as_view({'get': 'photo_ratings'}), name='photo-ratings'),
]
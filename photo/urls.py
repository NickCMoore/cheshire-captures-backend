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
    path('photos/<int:pk>/like/', LikeViewSet.as_view({'post': 'like'}), name='photo-like'),
    path('photos/<int:pk>/unlike/', LikeViewSet.as_view({'post': 'unlike'}), name='photo-unlike'),
]

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Photo, Tag, Like
from .serializers import PhotoSerializer, TagSerializer, LikeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

# Custom pagination class to control the number of items per page
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# ViewSet for handling CRUD operations for Photo model
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'category', 'photographer__display_name']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(photographer=self.request.user.photographer) 

# ViewSet for handling CRUD operations for Tag model
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

# ViewSet for handling CRUD operations for Like model
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(photographer=self.request.user.photographer)

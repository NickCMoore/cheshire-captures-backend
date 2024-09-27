from rest_framework import viewsets, permissions, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Photo, Tag, Like, Comment
from .serializers import PhotoSerializer, TagSerializer, LikeSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import PhotoFilter
from rest_framework.decorators import action
from rest_framework.response import Response

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
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['photographer__display_name', 'photo__title']
    filterset_fields = ['photo']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(photographer=self.request.user.photographer)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        try:
            photo = Photo.objects.get(pk=pk)
            photographer = request.user.photographer
            if Like.objects.filter(photo=photo, photographer=photographer).exists():
                return Response({'status': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
            Like.objects.create(photo=photo, photographer=photographer)
            return Response({'status': 'Photo liked'}, status=status.HTTP_201_CREATED)
        except Photo.DoesNotExist:
            return Response({'status': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        try:
            photo = Photo.objects.get(pk=pk)
            photographer = request.user.photographer
            like = Like.objects.filter(photo=photo, photographer=photographer)
            if not like.exists():
                return Response({'status': 'Not liked yet'}, status=status.HTTP_400_BAD_REQUEST)
            like.delete()
            return Response({'status': 'Photo unliked'}, status=status.HTTP_204_NO_CONTENT)
        except Photo.DoesNotExist:
            return Response({'status': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

# ViewSet for handling CRUD operations for Comment model
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['content', 'photographer__display_name']
    filterset_fields = ['photo']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(photographer=self.request.user.photographer)


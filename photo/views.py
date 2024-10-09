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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PhotoFilter
    search_fields = ['title', 'description', 'category', 'photographer__display_name']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        return Photo.objects.all().order_by('-rating')

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path='rate')
    def rate_photo(self, request, pk=None):
        photo = self.get_object()
        rating = request.data.get('rating')
        if rating is not None:
            try:
                rating = float(rating)
                if 0 <= rating <= 5: 
                    total_rating = (photo.rating * photo.rating_count) + rating
                    photo.rating_count += 1
                    photo.rating = total_rating / photo.rating_count
                    photo.save()
                    return Response({'detail': 'Rating added successfully!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Rating should be between 0 and 5.'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'detail': 'Invalid rating value.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Rating not provided.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='top-rated')
    def top_rated(self, request):
        top_photos = self.get_queryset().order_by('-rating')[:10]
        page = self.paginate_queryset(top_photos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(top_photos, many=True)
        return Response(serializer.data)

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

    def get_queryset(self):
        photo_id = self.kwargs.get('photo_id')
        if photo_id:
            return self.queryset.filter(photo_id=photo_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        photo_id = kwargs.get('photo_id')
        if not photo_id:
            return Response({'detail': 'Photo ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            photo = Photo.objects.get(id=photo_id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(photo=photo, photographer=request.user.photographer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Photo.DoesNotExist:
            return Response({'detail': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

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
from django.shortcuts import get_object_or_404

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
        """
        Optionally restricts the returned photos to the logged-in user or filter by category.
        """
        queryset = Photo.objects.all().order_by('-rating')
        user = self.request.user

        if self.action == 'my_photos' and user.is_authenticated:
            return queryset.filter(photographer=user.photographer)

        return queryset

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_photos(self, request):
        """
        Retrieves photos uploaded by the currently authenticated user.
        """
        photographer = request.user.photographer
        photos = self.get_queryset().filter(photographer=photographer)
        page = self.paginate_queryset(photos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(photos, many=True)
        return Response(serializer.data)

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
        """
        Returns the top-rated photos.
        """
        top_photos = self.get_queryset().order_by('-rating')[:10]
        page = self.paginate_queryset(top_photos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(top_photos, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(photographer=self.request.user.photographer)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

from rest_framework import viewsets, permissions, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Photo, Tag, Like, Comment, PhotoRating
from .serializers import PhotoSerializer, TagSerializer, LikeSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import PhotoFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from photographers.models import Photographer

# Custom pagination class to control the number of items per page
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# ViewSet for handling CRUD operations for Photo model
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
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

    def destroy(self, request, *args, **kwargs):
        photo = self.get_object()
        if photo.photographer.user != request.user:
            return Response({'error': 'You do not have permission to delete this photo.'}, status=403)
        return super().destroy(request, *args, **kwargs)

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
        rating_value = request.data.get('rating')
        user = request.user

        if rating_value is not None:
            try:
                rating_value = int(rating_value)
                if 1 <= rating_value <= 5:
    
                    user_rating, created = PhotoRating.objects.get_or_create(user=user, photo=photo)
                    
              
                    if not created:
                        old_rating = user_rating.rating
                        user_rating.rating = rating_value
                        user_rating.save()

              
                        total_rating = (photo.rating * photo.rating_count) - old_rating + rating_value
                    else:
                        total_rating = (photo.rating * photo.rating_count) + rating_value
                        photo.rating_count += 1

              
                    photo.rating = total_rating / photo.rating_count
                    photo.save()

                    return Response({'detail': 'Rating added or updated successfully!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Rating should be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)
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

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticatedOrReadOnly], url_path='ratings')
    def photo_ratings(self, request, pk=None):
        """
        Retrieves all ratings for a specific photo.
        """
        photo = self.get_object()
        ratings = PhotoRating.objects.filter(photo=photo)
        serializer = PhotoRatingSerializer(ratings, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(photographer=self.request.user.photographer)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



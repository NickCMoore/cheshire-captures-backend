from datetime import datetime
from django.db.models import F
from django.utils.timezone import make_aware
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Photo, Tag, Like, Comment, PhotoRating
from .serializers import (
    PhotoSerializer,
    TagSerializer,
    LikeSerializer,
    CommentSerializer,
    PhotoRatingSerializer,
)
from .filters import PhotoFilter


# Pagination for photos
class PhotoPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


# List and create photos
class PhotoListCreateView(generics.ListCreateAPIView):
    queryset = Photo.objects.all().order_by('-created_at')
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PhotoPagination
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PhotoFilter
    search_fields = ['title', 'description', 'category', 'photographer__username']
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        serializer.save(photographer=self.request.user)


# Retrieve, update, and delete photos
class PhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        photo = self.get_object()
        if photo.photographer != request.user:
            return Response(
                {'error': 'You do not have permission to delete this photo.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().delete(request, *args, **kwargs)


# View for listing the user's own photos, with date filtering
class MyPhotosListView(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PhotoPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Photo.objects.filter(photographer=user)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            try:
                start_date_with_time = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
                queryset = queryset.filter(created_at__gte=start_date_with_time)
            except ValueError:
                pass

        if end_date:
            try:
                end_date_with_time = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
                queryset = queryset.filter(created_at__lte=end_date_with_time)
            except ValueError:
                pass

        return queryset


# List the top-rated photos
class TopRatedPhotosView(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PhotoPagination

    def get_queryset(self):
        return Photo.objects.order_by('-rating')[:10]


# Submit a rating for a photo
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    rating_value = request.data.get('rating')

    try:
        rating_value = int(rating_value)
        if not (1 <= rating_value <= 5):
            return Response({'detail': 'Rating must be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

        user_rating, created = PhotoRating.objects.get_or_create(user=request.user, photo=photo)
        if not created:
            # Update existing rating
            old_rating = user_rating.rating
            user_rating.rating = rating_value
            user_rating.save()
            photo.rating_count = F('rating_count')
            photo.rating = (F('rating') * F('rating_count') - old_rating + rating_value) / F('rating_count')
        else:
            # Add new rating
            user_rating.rating = rating_value
            user_rating.save()
            photo.rating_count = F('rating_count') + 1
            photo.rating = (F('rating') * (F('rating_count') - 1) + rating_value) / F('rating_count')

        photo.save()
        return Response({'detail': 'Rating added or updated successfully!'}, status=status.HTTP_200_OK)
    except ValueError:
        return Response({'detail': 'Invalid rating value.'}, status=status.HTTP_400_BAD_REQUEST)


# Retrieve all ratings for a specific photo
class PhotoRatingsView(generics.ListAPIView):
    serializer_class = PhotoRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])
        return PhotoRating.objects.filter(photo=photo)


# Like photo view
class PhotoLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        user = request.user
        like_instance, created = Like.objects.get_or_create(user=user, photo=photo)

        if created:
            photo.likes_count += 1
            photo.save()
            return Response(
                {'status': 'liked', 'likes_count': photo.likes_count},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'detail': 'You have already liked this photo.'},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Unlike view
class PhotoUnlikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        user = request.user
        like_instance = Like.objects.filter(user=user, photo=photo).first()

        if like_instance:
            like_instance.delete()
            photo.likes_count -= 1
            photo.save()
            return Response(
                {'status': 'unliked', 'likes_count': photo.likes_count},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {'detail': 'You have not liked this photo yet.'},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Create and list tags for photos
class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


# Create and list likes for photos
class LikeListCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Create and list comments for photos
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        photo_id = self.kwargs.get('pk')
        photo = get_object_or_404(Photo, pk=photo_id)
        return Comment.objects.filter(photo=photo)

    def perform_create(self, serializer):
        photo_id = self.kwargs.get('pk')
        photo = get_object_or_404(Photo, pk=photo_id)
        serializer.save(user=self.request.user, photo=photo)


# Retrieve, update, and delete comments
class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.user != self.request.user and not self.request.user.is_staff:
            return Response(
                {"error": "You are not allowed to edit this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()

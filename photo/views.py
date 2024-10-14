from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.dateparse import parse_date
from django_filters.rest_framework import DjangoFilterBackend
from .models import Photo, Tag, Like, Comment, PhotoRating
from .serializers import PhotoSerializer, TagSerializer, LikeSerializer, CommentSerializer, PhotoRatingSerializer
from .filters import PhotoFilter
from django.shortcuts import get_object_or_404
from datetime import datetime

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
            return Response({'error': 'You do not have permission to delete this photo.'}, status=status.HTTP_403_FORBIDDEN)
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
                parsed_start_date = parse_date(start_date)
                if parsed_start_date:
                    start_date_with_time = datetime.combine(parsed_start_date, datetime.min.time())
                    queryset = queryset.filter(created_at__gte=start_date_with_time)
                else:
                    print(f"Error: Invalid start_date {start_date}")
            except ValueError as e:
                print(f"Error parsing start_date: {e}")

        if end_date:
            try:
                parsed_end_date = parse_date(end_date)
                if parsed_end_date:
                    end_date_with_time = datetime.combine(parsed_end_date, datetime.max.time())
                    queryset = queryset.filter(created_at__lte=end_date_with_time)
                else:
                    print(f"Error: Invalid end_date {end_date}")
            except ValueError as e:
                print(f"Error parsing end_date: {e}")

        print(f"Filtered queryset (count: {queryset.count()}): {queryset}")

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

    if rating_value is not None:
        try:
            rating_value = int(rating_value)
            if 1 <= rating_value <= 5:
                user_rating, created = PhotoRating.objects.get_or_create(user=request.user, photo=photo)
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

# Retrieve all ratings for a specific photo
class PhotoRatingsView(generics.ListAPIView):
    serializer_class = PhotoRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])
        return PhotoRating.objects.filter(photo=photo)

# Like/Unlike photo view
class PhotoLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        user = request.user
        like_instance = Like.objects.filter(user=user, photo=photo).first()

        if like_instance:
            like_instance.delete()
            if photo.likes_count > 0:
                photo.likes_count -= 1
            photo.save()
            return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Like photo
            Like.objects.create(user=user, photo=photo)
            photo.likes_count += 1
            photo.save()
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)




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

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Get comments for the specific photo
    def get_queryset(self):
        photo_id = self.kwargs.get('pk')
        photo = get_object_or_404(Photo, pk=photo_id)
        print(f"Fetching comments for photo ID: {photo.pk}") 
        return Comment.objects.filter(photo=photo)

    # Add a new comment for the specific photo
    def perform_create(self, serializer):
        photo_id = self.kwargs.get('pk')
        photo = get_object_or_404(Photo, pk=photo_id)
        print(f"Adding comment to photo ID: {photo.pk}") 
        serializer.save(user=self.request.user, photo=photo)

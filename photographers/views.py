from rest_framework import viewsets, permissions, filters, generics
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Photographer, Follow
from .serializers import PhotographerSerializer, FollowSerializer
from .permissions import IsOwnerOrReadOnly


# Custom pagination class for photographers
class PhotographerPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_page_size(self, request):
        # Return the custom page size if specified in request, but limit to max_page_size
        page_size = super().get_page_size(request)
        return min(page_size, self.max_page_size) if page_size else self.page_size


# ViewSet for Photographer model
class PhotographerViewSet(viewsets.ModelViewSet):
    queryset = Photographer.objects.select_related('user').prefetch_related('followers')
    serializer_class = PhotographerSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PhotographerPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'display_name']
    search_fields = ['display_name', 'bio', 'location']
    ordering_fields = ['created_at', 'display_name']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ViewSet for Follow model with custom unfollow action
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user.photographer)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk=None):
        following = self.get_photographer_object(pk)
        if not following:
            return Response({'error': 'Photographer not found'}, status=404)
        
        follow_instance = self.get_follow_instance(request.user.photographer, following)
        if not follow_instance:
            return Response({'error': 'Not following'}, status=400)
        
        follow_instance.delete()
        return Response({'status': 'unfollowed'})

    def get_photographer_object(self, pk):
        try:
            return Photographer.objects.get(pk=pk)
        except Photographer.DoesNotExist:
            return None

    def get_follow_instance(self, follower, following):
        try:
            return Follow.objects.get(follower=follower, following=following)
        except Follow.DoesNotExist:
            return None


# View for listing top photographers based on follower count
class TopPhotographersView(generics.ListAPIView):
    serializer_class = PhotographerSerializer
    pagination_class = PhotographerPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Photographer.objects.annotate(
            follower_count=Count('followers')
        ).order_by('-follower_count')

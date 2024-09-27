from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Photographer, Follow
from .serializers import PhotographerSerializer, FollowSerializer
from .permissions import IsOwnerOrReadOnly


class PhotographerPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class PhotographerViewSet(viewsets.ModelViewSet):
    queryset = Photographer.objects.all()
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

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user.photographer)

    @action(detail=True, methods=['POST'])
    def unfollow(self, request, pk=None):
        try:
            following = Photographer.objects.get(pk=pk)
            follow_instance = Follow.objects.get(follower=request.user.photographer, following=following)
            follow_instance.delete()
            return Response({'status': 'unfollowed'})
        except Follow.DoesNotExist:
            return Response({'error': 'Not following'}, status=400)

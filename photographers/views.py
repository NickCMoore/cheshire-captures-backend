from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Count
from django.http import Http404
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
        page_size = super().get_page_size(request)
        return min(page_size, self.max_page_size) if page_size else self.page_size

# List view for photographers
class PhotographerList(generics.ListAPIView):
    queryset = Photographer.objects.annotate(total_followers=Count('followers'))
    serializer_class = PhotographerSerializer
    pagination_class = PhotographerPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['total_followers', 'created_at']

    def get_queryset(self):
        return Photographer.objects.annotate(
            total_followers=Count('followers')
        ).order_by('-total_followers')

# Detail view for a single photographer
class PhotographerDetail(generics.RetrieveUpdateAPIView):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.serializer_class(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.serializer_class(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Photographer
from .serializers import PhotographerSerializer
from .permissions import IsOwnerOrReadOnly

class PhotographerPagination(PageNumberPagination):
    page_size = 10  # Number of photographers to display per page
    page_size_query_param = 'page_size'
    max_page_size = 50

class PhotographerList(generics.ListCreateAPIView):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Anyone can view, but only authenticated users can create
    pagination_class = PhotographerPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location', 'display_name']  # Filter photographers by location or name

    def perform_create(self, serializer):
        # Set the user field to the current authenticated user
        serializer.save(user=self.request.user)

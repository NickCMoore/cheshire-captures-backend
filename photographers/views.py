from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PhotographerPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location', 'display_name']  # Apply filters to queryset

    def perform_create(self, serializer):
        # Set the user field to the current authenticated user
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # Custom list method to include pagination and filtering in response
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Update the detail view if needed:
class PhotographerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer
    permission_classes = [IsOwnerOrReadOnly]

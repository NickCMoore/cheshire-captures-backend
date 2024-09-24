from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Photographer
from .serializers import PhotographerSerializer
from .permissions import IsOwnerOrReadOnly


class PhotographerPagination(PageNumberPagination):
    page_size = 10  # Number of photographers to display per page
    page_size_query_param = 'page_size'
    max_page_size = 50


class PhotographerList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Anyone can view, but only authenticated users can create

    def get(self, request):
        # Retrieve and filter photographers
        photographers = Photographer.objects.all()
        filter_backends = [DjangoFilterBackend]
        filterset_fields = ['location', 'display_name']  # Apply filters to queryset
        paginator = PhotographerPagination()
        result_page = paginator.paginate_queryset(photographers, request)
        serializer = PhotographerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        # Create a new photographer
        serializer = PhotographerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
